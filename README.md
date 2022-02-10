# video-copyright-lite
video copyright protector based on digital watermark

---

# BaseLine

---
### 2022/1/12
>  使用 [StegaStamp](https://github.com/linzissu/StegaStamp) 和 [OpenCV](https://opencv.org/) 给一条视频加入一段文字 (大于7个字符).然后再将视频解码成文字
- video/IO: [Learn to read video, display video, and save video.](https://docs.opencv.org/4.x/dd/d43/tutorial_py_video_display.html)
- [StegaStamp](https://github.com/linzissu/StegaStamp)
- Kaggle
- video

---
### 2022/1/26
> 搭建Flutter环境， 运行第一个Demo
- Flutter 官网: [https://flutter.cn/](https://flutter.cn/)
- 环境搭建: [https://flutter.cn/docs/get-started/install/windows](https://flutter.cn/docs/get-started/install/windows)
- 编写第一个Flutter应用：[https://flutter.cn/docs/get-started/codelab](https://flutter.cn/docs/get-started/codelab)
- Flutter Online: [https://flutlab.io/editor/](https://flutlab.io/editor/)

---
### 2022/2/08
> 模型转换
- API：[https://www.tensorflow.org/lite/convert?hl=zh-cn](https://www.tensorflow.org/lite/convert?hl=zh-cn)
- 新建 `models/convert.py`

---
### 2022/2/10
> 模型接入
> ![image](https://user-images.githubusercontent.com/60593268/153334373-529c767d-7a74-4613-a58f-45692ac45456.png)

- 参考 tflite_flutter：[tflite_flutter: ^0.9.0](https://pub.dev/packages/tflite_flutter)
- 参考 [tflite_flutter_helper](https://github.com/am15h/tflite_flutter_helper)
- bchlib：参考[bchlib-api](#) 和 [dio: ^4.0.4](https://pub.dev/packages/dio)

