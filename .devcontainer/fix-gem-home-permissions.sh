#!/usr/bin/env bash
# Repair write access to the shared gem home for the non-root dev user.
#
# The Jekyll dev container image installs Jekyll, Bundler and github-pages
# *as root* during the image build, so the subdirectories of GEM_HOME
# (/usr/local/bundle) are left owned by root:root with mode 755 - only the
# top-level directory itself is 1777. A `bundle install` running as the
# non-root "vscode" user therefore fails with
#   Bundler::PermissionError ... /usr/local/bundle/cache/<gem>.gem
# whenever the Gemfile needs a gem the image does not ship (e.g. logger, csv
# or uri, which Ruby 3.3 only ships as bundled - not installed - gems).
#
# Fix it the same way the image itself is being fixed upstream
# (https://github.com/devcontainers/images/pull/1991): hand the tree to the
# "ruby" group that "vscode" is already a member of, make it group writable
# and set the setgid bit on the directories so gems installed later keep
# inheriting that group.
#
# The script is idempotent, so it is safe to run via both postCreateCommand
# and postStartCommand: if everything is already writable it only performs a
# cheap writability probe and does nothing, otherwise it repairs the tree
# and then verifies the repair before letting the caller proceed to
# `bundle install`.
set -euo pipefail

GEM_HOME_DIR="${GEM_HOME:-/usr/local/bundle}"

writable_tree() {
	# Every subdirectory bundler or gem may write to must exist and be
	# writable for the calling (non-root) user. `bin` is included because
	# installing a gem drops its executables there.
	local dir
	for dir in "$GEM_HOME_DIR"/ "$GEM_HOME_DIR"/bin "$GEM_HOME_DIR"/build_info \
		"$GEM_HOME_DIR"/cache "$GEM_HOME_DIR"/doc "$GEM_HOME_DIR"/extensions \
		"$GEM_HOME_DIR"/gems "$GEM_HOME_DIR"/plugins "$GEM_HOME_DIR"/specifications; do
		if [ ! -d "$dir" ] || [ ! -w "$dir" ]; then
			return 1
		fi
	done
	return 0
}

if writable_tree; then
	exit 0
fi

echo "fix-gem-home-permissions: $GEM_HOME_DIR is not writable, repairing ownership with sudo..." >&2

# Requires passwordless sudo, which the dev container grants the vscode user.
sudo chgrp -R ruby "$GEM_HOME_DIR"
sudo chmod -R g+rwX "$GEM_HOME_DIR"
sudo find "$GEM_HOME_DIR" -type d -exec chmod g+s {} +

if ! writable_tree; then
	echo "fix-gem-home-permissions: ERROR: $GEM_HOME_DIR is still not writable after the repair." >&2
	echo "fix-gem-home-permissions: Run 'Rebuild Container' so postCreateCommand runs again," >&2
	echo "fix-gem-home-permissions: or fix the permissions manually as root." >&2
	exit 1
fi

echo "fix-gem-home-permissions: $GEM_HOME_DIR is now writable." >&2
