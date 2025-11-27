# 📝 StoryCraft — Multiplayer Story Builder

<p align="center">
  <img src="https://img.shields.io/badge/Platform-Android-brightgreen?style=for-the-badge&logo=android" alt="Platform Android"/>
  <img src="https://img.shields.io/badge/Kotlin-1.9+-purple?style=for-the-badge&logo=kotlin" alt="Kotlin"/>
  <img src="https://img.shields.io/badge/Jetpack%20Compose-Material3-blue?style=for-the-badge&logo=jetpackcompose" alt="Jetpack Compose"/>
  <img src="https://img.shields.io/badge/Firebase-Backend-orange?style=for-the-badge&logo=firebase" alt="Firebase"/>
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License MIT"/>
</p>

<p align="center">
  <strong>🌍 A collaborative, multiplayer story-building app where friends take turns writing a story together — line by line — in real time.</strong>
</p>

---

## 🎯 Purpose / Vision

**StoryCraft** is inspired by campfire storytelling, improv games, and writing prompts. The app gamifies creativity and makes storytelling **fun, social, and unpredictable**.

### Our Goals:
- ✨ **Encourages creativity** — Unleash your imagination with friends
- 🌐 **Connects friends locally or globally** — Play with anyone, anywhere
- 🎮 **Provides fun writing games** — Turn-based collaborative storytelling
- 💎 **Looks premium and modern** — Apple-style glassmorphism UI
- 🛠️ **Demonstrates real-world Android development skills** — Firebase + Compose + Clean Architecture

---

## 🌍 How the App Works (Flow)

### 1️⃣ Login
The user logs in using **Google Sign-In**.  
Firebase Authentication handles secure sign-in and user sessions.

### 2️⃣ Home Screen
After login, the user sees a **premium Apple-style UI** with:
- 👤 Profile greeting
- 🃏 Four action cards:
  - **Create Room**
  - **Join Room**
  - **My Stories**
  - **Inspirations**
- 🌟 Glassmorphism floating cards
- ✨ Animations and smooth transitions
- 📱 Floating bottom navigation

### 3️⃣ Create Room
User can:
- 🔑 Generate a unique room code
- 📨 Invite friends
- 👑 Become the "host" of the session

**The host controls:**
- ▶️ Starting the story
- 🔄 Managing player turns
- 🛑 Ending the session

Room data is stored in **Firestore**.

### 4️⃣ Join Room
Friends enter a **6-digit room code** to join the host.  
All players appear in a "lobby" UI.

### 5️⃣ Multiplayer Story Mode
Players take turns writing **one line of a story**.

**Real-time behavior:**
- ⚡ When a player submits a line, Firestore updates instantly
- 📡 All players receive real-time story updates
- 🎯 App shows turn order
- 💬 UI displays the story as a chat timeline
- ⌨️ Fancy typing animation shows when a player is writing

### 6️⃣ Story Completion
When the story ends:
- 💾 The final story is saved in Firestore
- 📚 User can access it later in "My Stories"
- 📤 Optionally export as:
  - 📄 PDF
  - 🔗 Shareable link
  - 📷 Instagram-friendly image

### 7️⃣ Inspirations (AI-Assisted Prompts)
The "Inspirations" screen gives:
- 🎲 Random story prompts
- 👥 Character ideas
- 🏞️ Setting ideas
- 🔀 Plot twists
- 🎯 Writing challenges

*(Can later integrate free AI APIs)*

### 8️⃣ Offline / Local Multiplayer (Future)
The app can also support **Nearby Connections API** for:
- 📶 Bluetooth story sessions
- 🖧 Offline LAN play

*(Optional stretch feature)*

---

## 🔥 Core Features

| Feature | Status |
|---------|--------|
| ✅ Google Sign-In Authentication | ✔️ |
| ✅ Beautiful Apple-style UI (glassmorphism + animations) | ✔️ |
| ✅ Real-time multiplayer rooms (Firestore) | ✔️ |
| ✅ Collaborative story writing | ✔️ |
| ✅ Turn-based gameplay | ✔️ |
| ✅ Saved stories library | ✔️ |
| ✅ AI-based inspiration prompts | ✔️ |
| ✅ Modern UI architecture (Compose + Material3 + animations) | ✔️ |
| ✅ Navigation using Jetpack Compose Navigation | ✔️ |
| ✅ Clean architecture and scalable code | ✔️ |

---

## ⚙️ Tech Stack

### 📱 Frontend
| Technology | Purpose |
|------------|---------|
| **Kotlin** | Primary programming language |
| **Jetpack Compose** | Modern declarative UI toolkit |
| **Material 3** | Design system and theming |
| **Compose Navigation** | Screen navigation |
| **Lottie Animations** | Rich animations |
| **Coil** | Image loading library |

### ☁️ Backend
| Technology | Purpose |
|------------|---------|
| **Firebase Authentication** | Google Sign-In |
| **Firebase Firestore** | Real-time stories + room sync |
| **Firebase Storage** | Story exports (optional) |

### 🏗️ Architecture
| Pattern | Description |
|---------|-------------|
| **MVVM** | Model-View-ViewModel pattern |
| **State Hoisting** | Compose state management |
| **ViewModel + Mutable State** | Reactive UI updates |
| **Firestore Snapshot Listeners** | Real-time data sync |

---

## 🏛️ Project Structure

```
app/
 ├── ui/
 │    ├── LoginScreen.kt           # Google Sign-In screen
 │    ├── HomeScreen.kt            # Main dashboard with action cards
 │    ├── CreateRoomScreen.kt      # Room creation and hosting
 │    ├── JoinRoomScreen.kt        # Join room via code
 │    ├── StoryScreen.kt           # Real-time collaborative writing
 │    ├── MyStoriesScreen.kt       # Saved stories library
 │    ├── InspirationsScreen.kt    # AI prompts and ideas
 │    └── components/
 │          ├── GlassCard.kt       # Glassmorphism card component
 │          ├── AnimatedHeader.kt  # Animated header component
 │          └── BottomBar.kt       # Floating bottom navigation
 │
 ├── navigation/
 │       └── Navigation.kt         # Compose navigation graph
 │
 ├── data/
 │       └── FirestoreRepository.kt # Firestore data operations
 │
 ├── model/
 │       └── StoryModel.kt         # Data models
 │
 ├── MainActivity.kt               # Entry point
 └── build.gradle.kts              # Dependencies configuration
```

---

## 🚀 Getting Started

### Prerequisites
- Android Studio Hedgehog (2023.1.1) or later
- Kotlin 1.9+
- JDK 17+
- Firebase project configured

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/DEADSAW/StoryCraft.git
cd StoryCraft
```

2. **Set up Firebase**
   - Create a new Firebase project at [Firebase Console](https://console.firebase.google.com/)
   - Enable **Authentication** (Google Sign-In)
   - Enable **Cloud Firestore**
   - Download `google-services.json` and place it in the `app/` directory

3. **Open in Android Studio**
   - File → Open → Select the cloned folder
   - Let Gradle sync complete

4. **Run the app**
   - Connect an Android device or start an emulator
   - Click **Run** ▶️

---

## 📱 Screenshots

> *Coming soon! Screenshots of the app UI will be added here.*

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 💖 Acknowledgments

- Inspired by campfire storytelling and improv games
- Built with ❤️ using modern Android development practices
- Thanks to the Jetpack Compose and Firebase teams for amazing tools

---

## 📞 Contact

For questions, suggestions, or collaboration:

- 📧 GitHub: [@DEADSAW](https://github.com/DEADSAW)

---

<p align="center">
  <strong>✨ "Stories connect us. Let's write them together." ✨</strong>
</p>

<p align="center">
  ⭐ Star this repo if you find it useful!
</p>
