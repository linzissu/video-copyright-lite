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

---
### 2022/2/26
> 完善模型接入：

- 已完成encode部分，接下来需要参照python代码部分完善[输出图像处理](https://github.com/linzissu/video-copyright-lite/blob/b77a030955952c67982b0c7932c59017f5e0f5b1/video_stega_stamp/encoder.py#L67)（out_img`*`255+0.5），最后将图片写入磁盘或展示在界面上。
- 参照encode编写好decode，验证是否编解码成功。
- 过程中可能会遇到图像旋转，RGB转换，格式转换等问题。
- 接入视频流，将单张图片扩展到视频流。

> 参考：
- [flutter_ffmpeg: ^0.4.2](https://pub.dev/packages/flutter_ffmpeg)
- [export_video_frame: ^0.0.7](https://pub.dev/packages/export_video_frame)

### 2022/4/1
> stega_stamp 后端
- [x] [File POST](https://flask.palletsprojects.com/en/2.0.x/patterns/fileuploads/)
- [ ] 前端设计界面，完成文件上传，编码，下载，上传，解码四个接口接入。[DIO](https://pub.dev/packages/dio)
