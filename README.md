### Trvium-Stream-Cipher

Trivium là một loại mã dòng đồng bộ hướng phần cứng

Trvivium được thiết kế như một bài tập nhằm khám phá mức độ đơn giản hóa mã dòng mà không ảnh hưởng đến tính bảo mật, tốc độ hay tính linh hoạt

Thuật toán tạo ra dãy giả ngẫu nhiên từ một khóa bí mật 80bit và một giá trị khởi tạo IV cũng 80bit

Các trạng thái trong gọi là Internal State có độ dài 288bit (s1, s2,..., s288)

Bộ tạo khóa là một quá trình trích xuất 15bit trạng thái nhất định và sử dụng chũng để cập nhật 3bit trạng thái và tính toán 1bit dòng khóa zi. Sau đó các bit trạng thái được quay và quá trình được lặp lại cho đến khi N <= 2^64 do giới hạn của hệ thống máy tính nhưng thực ra ta chỉ cần lặp đến khi nào khóa có độ dài bằng bản rõ

Trước tiên ta cần có khởi tạo các giá trị của trạng thái trong từ các khóa bí mật K và IV như sau:

```
(s1, s2, ..., s93)        <--   (K1, K2, ..., K80, 0, ..., 0)
(s94, s95, ..., s177)     <--   (IV1, IV2, ..., IV80, 0, ..., 0)
(s178, s179, ..., s288)   <--   (0, 0, ..., 0, 1, 1 1)
```

Các trạng thái được xoay hết 4 chu kì như sau:

```
for i = 1 to 4 * 288 do:
  t1 = s66 + s91.s92 + s93 + s171
  t2 = s162 + s175.s176 + s177 + s264
  t3 = s243 + s286.s287 + s288 + s69
  (s1, s2, ..., s93)        <--   (t3, s1, ..., s92)
  (s94, s95, ..., s177)     <--   (t1, s94, ..., s176)
  (s178, s179, ..., s288)   <--   (t2, s178, ..., s287)
end for
```

Ảnh mô tả thuật toán tạo chuỗi khóa:

![image](https://user-images.githubusercontent.com/115722174/200348022-8b356fa9-a222-4391-a57c-aa883f769187.png)

Từ đó ta có thuật toán tạo chuỗi khóa z như sau:

```
for i = 1 to N do:
  k1 = s66 + s93
  k2 = s162 + s177
  k3 = s243 + s288
  zi = k1 + k2 + k3
  t1 = k1 + s91.s92 + s171
  t2 = k2 + s175.s176 + s264
  t3 = k3 + s286.s287 + s69
  (s1, s2, ..., s93)        <--   (t3, s1, ..., s92)
  (s94, s95, ..., s177)     <--   (t1, s94, ..., s176)
  (s178, s179, ..., s288)   <--   (t2, s178, ..., s287)
end for
```

### Example

Giả sử ta có khóa bí mật K có 20 kí tự hexa như sau: ```K = '0F62B5085BAE0154A7FA'```

Và một giá trị khởi tạo IV cũng có 20 kí tự hexa đảm bảo K và IV đều tạo ra một chuỗi có 80bit ```IV = '288FF65DC42B92F960C7'```

khi đó ta sẽ được chuỗi bit của K và IV tương ứng là:

```
K_bits = [1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0,
          0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1]
IV_bits = [1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1,
           1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0]
```

Từ đó ta được chuỗi S ban đầu, sau khi quay hết 4 chu kì ta được chuỗi S như sau

```
S = [0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0,
     0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1,
     1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1,
     1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1,
     1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1,
     0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1,
     0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1]
```

Sau khi thực hiện tạo khóa z thì ta được Key Stream dạng Hexa là 

```Key Stream = 'A4386C6D7624983FEA8DBE7314E5FE1F9D102004C2CEC99AC3BFBF003A66433F3089A98FAD8512C49D7A'```

Với ```Plaintext = 'Hanoi University of Science and Technology'``` ta được ```Ciphertext = 'ìYÍQûÛgf½F$­ ÿ­ÜÚ ['dìÊçÃê~«ú'```

### Tài liệu tham khảo
<https://www.ecrypt.eu.org/stream/p3ciphers/trivium/trivium_p3.pdf>
