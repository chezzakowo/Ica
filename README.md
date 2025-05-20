> [!CAUTION]
>Phần mềm này được phát triển chỉ với mục đích giải trí (Just For Fun - J4F), không phải là phần mềm gian lận hay can thiệp vào game. Mọi hành động bạn thực hiện khi sử dụng phần mềm này (bao gồm chỉnh sửa, làm tăng tải CPU, RAM, hoặc bất kỳ tác động nào ảnh hưởng đến máy tính hoặc game, tài khoản game của bạn) đều do bạn tự chịu trách nhiệm. Mình sẽ không chịu bất kỳ trách nhiệm nào liên quan đến những vấn đề phát sinh!

<p align="center">
  <img src="./docs/img/header.png" alt="I'm just a header with a meme">
</p>

<h1 align="center">🦄 Ica 🦄</h1>

**Ica** là một dự án mà mình viết ra dựa trên việc cộng động Honkai: Star Rail trên [Reddit](https://www.reddit.com/r/HonkaiStarRail/comments/1kj1reu/guys_im_kinda_new_here_why_the_hell_are_we/) và [HSR Việt Nam](https://www.facebook.com/tempest.ru/posts/trung-b%C3%ACnh-meme-v%E1%BB%81-ica-b%C3%AAn-reddit-ki%E1%BB%83uhsr/624960197253440/) cũng như là trên TikTok và Youtube joke về việc Ica bell ăn luôn cả Hyacine (theo mình biết tại mình chưa cày cốt truyện tới đó) khá là nhiều thế nên là mình viết phần mềm nay ra cũng chỉ để "đùa" theo thôi!

Dự án này hoạt động như sau: Khi phát hiện tiến trình StarRail.exe (Client game) đang chạy, phần mềm sẽ thực hiện một số phép tính nhằm tăng tải CPU và RAM, nhằm “giả bộ” như thể Ica bell đang “ăn hết” tài nguyên máy bạn vậy. Bên cạnh đó, nó còn phát ra một trong ba hiệu ứng liên quan đến Ica như Ica ngồi sập máy tính bạn, rơi cửa sổ,... Có thể coi công cụ này như một phần mềm test hiệu năng “kiểu joke” cũng được! (chắc thế)

--- 

## 📖 Mục lục
- [🔧 Cài đặt](#-cài-đặt)
- [🚀 Cách sử dụng](#-cách-sử-dụng)
  - [🚩Tham số phụ](#-tham-số-phụ)
- [🎭 Hiệu ứng](#-hiệu-ứng)
- [🎥 Demo video](#-demo-video)
- [🎲 Xác suất của việc "spawn" và hiệu ứng](#-xác-suất-"spawn"-và-hiệu-ứng)
- [⚠️ Lưu ý và trách nhiệm](#-lưu-ý-và-trách-nhiệm)
- [🔄 Phiên bản và cập nhật](#-phiên-bản-cập-nhật)
- [🤝 Đóng góp và phản hồi](#-đóng-góp-và-phản-hồi)

---

## 🔧 Cài đặt
- **Phương án 1 (Chạy trực tiếp)**: Tải file **Ica.exe** [tại đây](https://github.com/chezzakowo/Ica/releases/download/release/Ica.exe) hoặc ở mục [**Release**](https://github.com/chezzakowo/Ica/releases/tag/release)

- **Phương án 2 (Tự build, tự chạy)**: 

**Bước 1**: Clone repo này về thư mục của bạn sau đó chuyển vào thư mục
```bash
git clone https://github.com/chezzakowo/Ica.git
cd Ica
cd src
```

**Bước 2**: Cài các thư viện cần thiết
```bash
pip install -r requirements.txt
```

## 🚀 Cách sử dụng

- **Đối với chạy trực tiếp**: Nhấn đúp vào và chạy luôn
> [!TIP]
> Nếu như phần mềm báo lỗi gì đó hoặc khi game chạy mà nó hiển thị sai cách thì bạn có thể Chuột phải->Run as Admin (chạy dưới quyền quản trị)

- **Đối với việc tự sử dụng**: 
Chạy lệnh như sau:
```bash
python main.py
```

### 🚩 Tham số phụ

Cả 2 loại đều sử dụng chung 1 kiểu tham số nên mình sẽ viết chung chung nha!
```bash
<loại cài đặt> --stress (True/Flase) --effect (True/Flase) --cpuLimit (số nguyên) --ramLimit (số nguyên)
```
Trong đó:
- ``--stress <True/Flase>``: Dùng để bật / tắt tính năng tạo tải CPU và RAM
- ``--effect <True/Flase>``: Dùng để bật / tắt hiệu ứng khi game khởi động
- ``--cpuLimit <số nguyên>``: Nhận giá trị số giúp bạn điều chỉnh % CPU mà phần mềm có thể tạo tải lên máy bạn
- ``--ramLimit <số nguyên>``: Nhận giá trị số giúp bạn điều chỉnh % RAM mà phần mềm có thể tạo tải lên máy bạn

## 🎭 Hiệu ứng
Bạn có thể đọc tại [Hiệu ứng](../../docs/docs/hieu_ung.md) nha

## 🎲 Xác suất của việc "spawn" và hiệu ứng

| ❗ Tên biến cố         | Spawn Ica (kích hoạt stress, effect, ...) | Hiệu ứng "Rơi còn Ica" | Hiệu ứng "Rơi mất Ica" | Hiệu ứng "Rơi dạng cửa sổ" |
|-----------------------|-------------------------------------------|------------------------|------------------------|----------------------------|
| 🎲 Tỉ lệ               | 0.90                                      | 1/3                    | 1/3                    | 1/3                        |
| 🔢Xác suất của biến cố | 90%                                       | ~3.33%                 | ~3.33%                 | ~3.33%                     |

## ⚠️ Lưu ý và trách nhiệm

> [!IMPORTANT]
> "Ica" được tạo ra chỉ với mục đích giải trí (Just For Fun). Đây không phải là công cụ gian lận, can thiệp vào dữ liệu game hay gây ảnh hưởng file game Honkai: Star Rail.

- Phần mềm này không tương tác trực tiếp với client game, mà chỉ tự động tăng tải CPU và RAM khi phát hiện ``StarRail.exe`` đang chạy — mang tính chất "giả lập Ica bell ăn tài nguyên" như meme.

- Việc sử dụng phần mềm có thể khiến máy bạn lag, thiếu ổn định hoặc quạt kêu to nếu cấu hình không đủ hoặc đang chạy nhiều ứng dụng nặng. Hãy cân nhắc trước khi sử dụng.

Mình không chịu trách nhiệm với bất kỳ vấn đề nào phát sinh khi bạn sử dụng phần mềm, bao gồm (nhưng không giới hạn):

- Hư hỏng phần cứng (do nhiệt độ tăng cao)

- Treo máy, mất dữ liệu, crash game, crash máy

- Ảnh hưởng đến tài khoản game, nếu có sự hiểu nhầm từ hệ thống

Bạn hoàn toàn chịu trách nhiệm với mọi hành động liên quan đến phần mềm này — bao gồm việc chỉnh sửa, sử dụng sai mục đích, hay chia sẻ lại.

## 🔄 Phiên bản và cập nhật

Vì đây là meme nên chắc mình sẽ không liên tục cập nhật liên tục đâu vì meme nó khá dễ "chêt" nên mình chỉ cố gắng sửa lỗi thôi. Lâu lâu mình có thể thêm chức năng chăng?

## 🤝 Đóng góp 
Đây là những người đóng góp vô dự án! Bạn có thể đóng góp bằng cách báo lỗi và update nếu muốn nhe!

<a href="https://github.com/chezzakowo/LunarSMP-Archive/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=chezzakowo/Ica" />
</a>


©️ Bản quyền tên và hình nhân vật bởi Hoyoverse. Dự án này không thề liên quan đến Hoyoverse hay là "công cụ chính thức"
