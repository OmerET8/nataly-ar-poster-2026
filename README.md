# 🎓 Interactive Academic Poster with MindAR (WebAR)

An Augmented Reality (AR) web application for academic conference poster presentations. Pointing a smartphone camera at static figures on the printed poster transforms them into looping simulation videos overlaid directly on top of the graphs—**with zero app installation required**.

---

## 🚀 Quick Start (Local Testing)

To test the application locally on your computer or local Wi-Fi:

1. **Start the local server:**
   ```bash
   python serve.py
   ```
2. **Access the tools in your browser:**
   - **Poster Mockup & QR Generator:** [http://localhost:8000/poster.html](http://localhost:8000/poster.html)
   - **WebAR Mobile Experience:** [http://localhost:8000/index.html](http://localhost:8000/index.html)
   - **Target Image Compiler:** [http://localhost:8000/compiler.html](http://localhost:8000/compiler.html)

3. **Test with your webcam:**
   Open [http://localhost:8000/index.html](http://localhost:8000/index.html) on your laptop/desktop, grant camera permission, and hold up `assets/graph1.png` or `assets/graph2.png` (on your phone screen or printed on paper) to the camera. The video overlay will immediately track and play!

---

## 🌐 Free Hosting on GitHub Pages (Recommended)

Mobile browsers (iOS Safari and Android Chrome) **strictly require HTTPS** for camera permissions (`getUserMedia`). **GitHub Pages** is completely free, includes automatic HTTPS, and requires no server maintenance.

### Step-by-Step Deployment (2 Minutes):

1. **Initialize Git and commit all files:**
   ```bash
   git init
   git add .
   git commit -m "Academic WebAR Poster with MindAR"
   ```

2. **Create a new GitHub repository:**
   - Go to [github.com/new](https://github.com/new).
   - Name your repository (e.g., `nataly-ar-poster` or `conference-ar`).
   - Keep it **Public** (required for free GitHub Pages).
   - Do **not** initialize with a README (we already have one).

3. **Push your code to GitHub:**
   ```bash
   git branch -M main
   git remote add origin https://github.com/<YOUR-GITHUB-USERNAME>/<YOUR-REPO-NAME>.git
   git push -u origin main
   ```

4. **Enable GitHub Pages:**
   - In your GitHub repository, click **Settings** (top tab).
   - In the left sidebar, click **Pages**.
   - Under **Build and deployment** > **Branch**:
     - Select `main` from the dropdown.
     - Select `/(root)` for the folder.
     - Click **Save**.
   - Within 1–2 minutes, your website will be live at:
     ```
     https://<YOUR-GITHUB-USERNAME>.github.io/<YOUR-REPO-NAME>/
     ```

5. **Generate your final Poster QR Code:**
   - Open [poster.html](file:///c:/Users/omere/Documents/technion/Bachelor/semester%206/nataly/poster.html) in your browser.
   - Enter your live GitHub Pages URL (e.g., `https://<YOUR-GITHUB-USERNAME>.github.io/<YOUR-REPO-NAME>/index.html`) in the top toolbar.
   - The QR code will update instantly.
   - Click **Save / Download QR Code** to use in PowerPoint / LaTeX / Illustrator, or click **Print / Save PDF** to print the entire poster!

---

## 📁 Project Architecture & Files

```text
├── index.html            # Main WebAR application (A-Frame + MindAR 1.2.5)
├── poster.html           # Academic conference poster mockup + live QR code generator
├── compiler.html         # 1-click in-browser MindAR targets compiler
├── serve.py              # Local development HTTP server with LAN IP detection
├── generate_assets.py    # Python script to generate sample scientific plots and H.264 MP4 videos
├── assets/
│   ├── targets.mind      # Compiled binary tracking features for both graphs (Target 0 & Target 1)
│   ├── graph1.png        # Figure 1: Temporal Signal Dynamics (Target 0)
│   ├── graph2.png        # Figure 2: Multi-Agent Convergence Landscape (Target 1)
│   ├── video1.mp4        # Video simulation overlay for Figure 1 (H.264, 16:9, muted loop)
│   ├── video2.mp4        # Video simulation overlay for Figure 2 (H.264, 16:9, muted loop)
│   └── sample-band/      # Backup sample multi-track test targets (band.mind)
└── README.md             # Project documentation
```

---

## 🎨 How to Swap in Your Real Research Graphs & Videos

When you are ready to use your actual research plots and videos:

1. **Save your graph images:**
   - Save your 2 figures as `assets/graph1.png` and `assets/graph2.png`.
   - *Recommendation:* Keep them at a 16:9 aspect ratio (e.g., 1280x720 or 1920x1080) for exact video alignment.

2. **Save your video animations:**
   - Save your 2 videos as `assets/video1.mp4` and `assets/video2.mp4`.
   - *Recommendation:* Encode using H.264 (`-c:v libx264 -pix_fmt yuv420p -movflags +faststart`) to ensure universal playback on mobile iOS Safari and Android Chrome without black screens.

3. **Recompile `targets.mind`:**
   - Open `compiler.html` in your browser.
   - Click on the Target 0 and Target 1 preview boxes to select your new graph images.
   - Click **⚡ Compile & Export targets.mind**.
   - Move the downloaded `targets.mind` file into the `assets/` folder, replacing the existing one.
   - Commit and push to GitHub!

---

## 💡 Best Practices for Academic Posters & AR Tracking

- **Feature Density:** MindAR extracts keypoints from high-contrast areas (axis tick marks, grid lines, text labels, markers, sharp corners). Avoid large solid white areas without details.
- **Paper Finish:** When printing the conference poster, choose **matte paper** or satin instead of high-gloss lamination. Glossy lamination causes intense light reflections under conference hall fluorescent lighting that can obstruct camera tracking.
- **QR Code Size:** The QR code on an A0/A1 poster should be at least **6 cm x 6 cm (2.5 in x 2.5 in)** so attendees can easily scan it from a comfortable standing distance (1–1.5 meters).
- **Video Orientation:** Align the width and height of `<a-video>` in [index.html](file:///c:/Users/omere/Documents/technion/Bachelor/semester%206/nataly/index.html) to the exact aspect ratio of your graph (e.g., `width="1" height="0.5625"` for 16:9).
