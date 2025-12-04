---
description: How to deploy Omni Realms to the Google Play Store
---

# Deploying to Google Play Store

## 1. Prerequisites
- A Google Play Developer Account ($25 one-time fee).
- A signed release of your app.

## 2. Create a Keystore
If you haven't already, generate a keystore file to sign your app.
**Run this in your terminal:**
```powershell
keytool -genkey -v -keystore c:\Users\Daniel\upload-keystore.jks -storetype JKS -keyalg RSA -keysize 2048 -validity 10000 -alias upload
```
*Keep this file safe! If you lose it, you can't update your app.*

## 3. Configure Signing in `android/key.properties`
Create a file named `key.properties` in the `android/` folder:
```properties
storePassword=<your-store-password>
keyPassword=<your-key-password>
keyAlias=upload
storeFile=c:/Users/Daniel/upload-keystore.jks
```

## 4. Update `android/app/build.gradle`
Ensure your `build.gradle` is configured to use the `key.properties` file for the release build type.

## 5. Build the App Bundle
Run the following command to build the release bundle:
```powershell
flutter build appbundle
```
The output file will be at: `build/app/outputs/bundle/release/app-release.aab`

## 6. Upload to Play Console
1. Go to [Google Play Console](https://play.google.com/console).
2. Create a new app.
3. Set up the store listing (title, description, screenshots).
4. Go to **Production** (or **Internal Testing** for a test run).
5. Upload the `app-release.aab` file.
6. Complete the content rating and target audience questionnaires.
7. Submit for review!
