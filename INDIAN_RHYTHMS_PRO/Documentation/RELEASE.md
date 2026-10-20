# Complete library release

Prepared release tag: `indian-rhythms-pro-v1.0.0`. This document does not assert that the tag, release, PR, or downloads are published. Confirm them on GitHub before sharing links.

The original ZIP is 3,024,955,570 bytes, exceeding GitHub's 2 GiB per-release-asset limit. It is prepared as three **byte-split parts of a single ZIP**, not three independent ZIP archives. Parts are at most 1 GiB: 1,073,741,824; 1,073,741,824; and 877,471,922 bytes. Keep these out of Git history.

Original ZIP SHA-256:

```text
8185e5f5a7ceaf1f15154efd79e1bfa1b502a1797a41495f1f40d2f8cc9d417c
```

## Download and reconstruct on macOS

After a maintainer publishes the release on `Jaspal84/eternal`, download all three `INDIAN_RHYTHMS_PRO.zip.part001` through `.part003` files, `SHA256SUMS`, and `INDIAN_RHYTHMS_PRO.zip.sha256` from the same release into a new empty directory. Do not download GitHub's automatically generated “Source code” archive expecting audio.

In Terminal, change to that directory and run:

```sh
shasum -a 256 -c SHA256SUMS
# Stop if ANY checksum fails. Do not continue with missing or mismatched parts.
# Ensure no existing reconstructed ZIP will be overwritten:
(test ! -e INDIAN_RHYTHMS_PRO.zip &&
 cat INDIAN_RHYTHMS_PRO.zip.part001 \
     INDIAN_RHYTHMS_PRO.zip.part002 \
     INDIAN_RHYTHMS_PRO.zip.part003 > INDIAN_RHYTHMS_PRO.zip)
shasum -a 256 -c INDIAN_RHYTHMS_PRO.zip.sha256
# Continue only if the reconstructed ZIP checksum is OK:
unzip -t INDIAN_RHYTHMS_PRO.zip
# Choose a new destination; preserve any existing installed library:
unzip -n INDIAN_RHYTHMS_PRO.zip -d ./Library-Installation
```

Allow at least 10 GB free for parts, reconstructed ZIP and extracted audio. Once checks succeed, Finder's Archive Utility can also open the reconstructed ZIP. Keep all original files until extraction is verified. See LOGIC_PRO.md for sample mapping; this is not an AU installer.

GitHub references (not fetched in this cloud network):
- https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases
- https://cli.github.com/manual/gh_release_create
- https://cli.github.com/manual/gh_release_upload

## Prepare and publish as a maintainer

This environment has prepared assets outside Git at `/workspace/release-assets/indian-rhythms-pro-v1.0.0`. To reproduce splitting without altering the original archive:

```sh
python3 INDIAN_RHYTHMS_PRO/Scripts/prepare_release.py \
  /workspace/INDIAN_RHYTHMS_PRO.zip \
  /workspace/release-assets/indian-rhythms-pro-v1.0.0
```

The output directory must not exist. The script verifies the concatenated input stream and rereads each part to check its hash. It does not modify the source archive.

Publishing requires authenticated GitHub API access with repository contents write permission; PR creation also needs pull-request write permission. Standard CLI use preserves configured authentication; do not embed tokens in scripts or documentation.

After reviewing/merging the source PR, choose the exact source commit to release. Substitute it for `SOURCE_COMMIT` below; do not accidentally release an unrelated default branch commit. These commands intentionally start with a draft and publish only after all assets upload:

```sh
ASSETS=/workspace/release-assets/indian-rhythms-pro-v1.0.0
TAG=indian-rhythms-pro-v1.0.0
gh release create "$TAG" --repo Jaspal84/eternal --target SOURCE_COMMIT \
  --title 'INDIAN RHYTHMS PRO v1.0.0' --draft \
  --notes-file INDIAN_RHYTHMS_PRO/Documentation/RELEASE_NOTES.md
gh release upload "$TAG" --repo Jaspal84/eternal \
  "$ASSETS/INDIAN_RHYTHMS_PRO.zip.part001" \
  "$ASSETS/INDIAN_RHYTHMS_PRO.zip.part002" \
  "$ASSETS/INDIAN_RHYTHMS_PRO.zip.part003" \
  "$ASSETS/SHA256SUMS" "$ASSETS/INDIAN_RHYTHMS_PRO.zip.sha256" \
  "$ASSETS/assets.json" "$ASSETS/RECONSTRUCT_MACOS.md"
gh release view "$TAG" --repo Jaspal84/eternal --json url,isDraft,assets
gh release edit "$TAG" --repo Jaspal84/eternal --draft=false
```

Stop on any command failure. If the tag/release already exists, inspect it before resuming rather than overwriting assets. Do not publish an incomplete draft. After publication, verify it is visible and not a draft, confirm asset sizes, and download each part from its actual `browser_download_url` into a separate directory; compare SHA-256 hashes with `assets.json`. A visible page or successful HEAD request alone does not prove complete byte integrity. Only report links as verified after the corresponding checks actually succeed.
