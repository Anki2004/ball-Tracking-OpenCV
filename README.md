# QuadBall Tracker 🔴🟢🔵🟡

## 🎥 Dynamic Multi-Color Ball Tracking Across Quadrants

QuadBall Tracker is an innovative computer vision project that brings the magic of object tracking to life! This Python-based application takes a video input and dynamically tracks balls of any color as they move across different quadrants of the frame. It's like having a smart, adaptable digital referee for your multi-dimensional game of catch!

### 🌟 Features

- 🔍 Automatically detects and tracks balls of any color
- 🎨 Uses advanced color clustering for flexible color recognition
- 🏁 Divides the video frame into four quadrants
- 📊 Records entry and exit events for each ball in every quadrant
- ⏱️ Provides timestamped data for all tracked events
- 🔄 Adapts to different lighting conditions and ball colors

## 🚀 How It Works

1. **Video Input**: Feed in your video of balls bouncing around.
2. **Color Detection**: Our smart algorithms use K-means clustering to identify distinct ball colors.
3. **Ball Tracking**: The system tracks the movement of each detected ball.
4. **Quadrant Mapping**: The video frame is split into four quadrants.
5. **Event Tracking**: The system records when balls enter or exit each quadrant.
6. **Data Output**: Get a detailed log of all ball movements!

## 🛠️ Technology Stack

- Python 3.x
- OpenCV for video processing and object detection
- NumPy for numerical operations
- scikit-learn for K-means color clustering
- Streamlit for the user interface

## 🏃‍♂️ Getting Started

1. Clone this repository
2. Install the required packages

## 🎮 Use Cases

- Analyze ball movement patterns in sports
- Create interactive art installations
- Develop physics simulations
- Enhance object tracking skills in computer vision
- Test color detection algorithms in various lighting conditions

## 🔧 Customization

- Adjust the number of colors to detect by modifying the `n_colors` parameter in the `detect_balls` function.
- Fine-tune ball detection sensitivity by adjusting the area threshold in the `detect_balls` function.

## 🤝 Contributing

We love contributions! If you have ideas to make QuadBall Tracker even more awesome, feel free to open an issue or submit a pull request.

## 📜 License

This project is open source and available under the MIT License.

---

Discover the colorful world of motion with QuadBall Tracker - now more flexible and powerful than ever! 🌈🏀✨
