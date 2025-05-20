Original: TT T,â,n B,ì,n,h Huyện Yên Sơn, Tuyên Quang (tăng ngram thì tốc độ xử lý tăng)
Ward -> Actual: 'Tân Tiến', Expected: 'Tân Bình'

Original: 357/28,Ng-T- Thuật,P1,Q3,TP.HồChíMinh. ('h.' bị xóa lúc preprocessing)
Province -> Actual: 'Ninh Thuận', Expected: 'Hồ Chí Minh'

Original: CH F1614-HH2-Khu ĐTM Dương Nội Yên NghĩahàdônghyàNội
Ward -> Actual: '', Expected: 'Yên Nghĩa'

Original: - Khu B Chu Hoà, Việt HhiPhú Thọ
Ward -> Actual: 'Bích Hòa', Expected: ''


Original: 31B Sư Vạn Hạnh, Phường 3 Quận 10, TP. Hồ Chí Minh (ưu tiên rightmost và kí tự số)
District -> Actual: '', Expected: '10'
Ward -> Actual: 'Tân Thành', Expected: '3'


Original: 191A Nguyễn Thị Định An Phú, Quận 2, Tp Hồ Chí Minh
District -> Actual: '', Expected: '2'


Original: XãBù Gia Mập,,T Bình Phước
District -> Actual: 'Bù Gia Mập', Expected: ''
Ward -> Actual: '', Expected: 'Bù Gia Mập'


Original:  Tam GiangNăm CănT.Cà Mau
District -> Actual: '', Expected: 'Năm Căn'
Ward -> Actual: '', Expected: 'Tam Giang'


Original: XTân Thạnh, hAn Minh (tách trie viết tắt và trie viết thường, ưu tiên trie viết thường trước)
Province -> Actual: 'Hồ Chí Minh', Expected: ''
District -> Actual: '', Expected: 'An Minh'
Ward -> Actual: 'Tân Thành', Expected: 'Tân Thạnh'


Original:  Hải An  Hải Lăng TQdung trị
Province -> Actual: '', Expected: 'Quảng Trị'

Original: P4 T.Ph9ốĐông Hà
District -> Actual: 'Hà Đông', Expected: 'Đông Hà'
Ward -> Actual: '', Expected: '4'

Original: F. Trần Hưng Đao,Phủ Ly,TỉnhH  Nam
Province -> Actual: '', Expected: 'Hà Nam'

Original: F.07, Q6, (Cân nhắc khi indexing số, ngoài thêm prefix, cần thêm số đó luôn)
Ward -> Actual: '', Expected: '07'

Original: xã Vạn Kim, HuyệnMỹ Đức, T.P HNội (hnoi -> ha noi có distance = 2)
Province -> Actual: '', Expected: 'Hà Nội'

Original: Thị trấnSông Đốc, , TnhCà Mau (có nên đưa 'Tnh' vào list cần preprocess không)
Province -> Actual: '', Expected: 'Cà Mau'
Slow execution (0.093s): X Vĩnh Hanh, Châu Thành,An Giang

Original: X. Sơn Hv HSơn Hoa Tỉnh Phú Yên
Ward -> Actual: 'Sơn Hà', Expected: 'Sơn Hội'

Original:  Thái Ha, HBa Vì, T.pHNội
Province -> Actual: '', Expected: 'Hà Nội'

