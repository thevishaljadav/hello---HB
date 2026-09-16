# Asia Drama — Google Play production checklist

## Code/build
- Target SDK: Android 16 / API 36.
- Release version: 2.3 / versionCode 6.
- Release uses R8/minification and resource shrinking.
- WebView JavaScript bridge is kept for the native player/billing bridge.
- External navigation is opened outside the WebView; SSL errors are rejected.
- Supabase JS is pinned to a specific SDK version.
- Razorpay web checkout is not loaded in the Play build; digital purchases use Google Play Billing.

## Backend/security
- Supabase account deletion Edge Function is active and JWT-protected.
- Public EXECUTE access was removed from `has_admin_access(uuid)` and `can_watch_episode(uuid, uuid)`.
- RLS is enabled on application tables.
- Supabase security advisors still report GraphQL schema exposure warnings and leaked-password protection disabled; review these before a large public rollout.

## Required before production submission
1. Configure the release keystore secrets in GitHub Actions:
   - `ANDROID_KEYSTORE_BASE64`
   - `ANDROID_KEYSTORE_PASSWORD`
   - `ANDROID_KEY_ALIAS`
   - `ANDROID_KEY_PASSWORD`
2. Build the signed AAB and verify it with `apksigner`.
3. Upload the signed AAB to Play Console internal testing first.
4. Test sign-in/sign-out, catalogue loading, series/season/episode navigation, free playback, paid episode purchase/restore, subscription access if enabled, watch progress, account deletion, and admin Studio access.
5. Provide Play Console App Access credentials/instructions if any production functionality requires sign-in.
6. Complete the Data safety form and content rating accurately.
7. Publish a public, non-geofenced privacy policy URL and a public account-deletion request URL. Add both to Play Console and keep them accessible after app installation/uninstallation.
8. If alternative billing is ever offered to India users, enroll in Google's India alternative billing program and implement its required APIs/reporting; otherwise keep Google Play Billing as the in-app digital payment path.
9. Confirm all launch content is licensed/owned and that posters, trailers, music and drama episodes have the necessary distribution rights.

## Current launch blockers
- The GitHub workflow can produce release artifacts without a keystore when secrets are absent, but those artifacts are **not production-submittable**. A signed AAB is required for the Play launch process.
- The external privacy-policy and account-deletion web resources must be publicly deployed and entered in Play Console; the app now provides an in-app account deletion path backed by the JWT-protected Supabase function.
- Production catalogue content and Google Play product IDs must be configured in Creator Studio/Play Console before a real-user launch.
