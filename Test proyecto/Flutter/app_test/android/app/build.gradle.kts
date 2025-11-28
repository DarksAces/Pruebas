plugins {
    id("com.android.application")
    id("kotlin-android")
    id("dev.flutter.flutter-gradle-plugin")
    id("com.google.gms.google-services") // <--- MUST BE PRESENT
}

android {
    // ⚠️ MODIFICACIÓN 1: Cambiar el namespace
    namespace = "com.example.app_test" 
    compileSdk = flutter.compileSdkVersion
    ndkVersion = flutter.ndkVersion

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    kotlinOptions {
        jvmTarget = JavaVersion.VERSION_17.toString()
    }

    defaultConfig {
        // ⚠️ MODIFICACIÓN 2: Cambiar el Application ID
        applicationId = "com.example.app_test" 
        // You can update the following values to match your application needs.
        // For more information, see: https://flutter.dev/to/review-gradle-config.
        minSdk = flutter.minSdkVersion
        targetSdk = flutter.targetSdkVersion
        versionCode = flutter.versionCode
        versionName = flutter.versionName
    }

    buildTypes {
        release {
            // TODO: Add your own signing config for the release build.
            // Signing with the debug keys for now, so `flutter run --release` works.
            signingConfig = signingConfigs.getByName("debug")
        }
    }
}

flutter {
    source = "../.."
}
dependencies {
    // ...
    implementation("com.google.firebase:firebase-firestore-ktx:24.10.0") // Ejemplo de versión conocida
    implementation("com.google.firebase:firebase-storage-ktx:20.3.0")    // Ejemplo de versión conocida
    // ...
}