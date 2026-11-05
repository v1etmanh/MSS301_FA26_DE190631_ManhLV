import docx
from docx.oxml import OxmlElement
from docx.text.paragraph import Paragraph

DATA = {
    "0.1": {
        "title": "TODO 0.1 Tạo thư mục gốc & docker-compose.yml",
        "result": "Cấu trúc thư mục dự án fu-cinema/ được khởi tạo chuẩn chỉnh. File docker-compose.yml khởi chạy thành công 3 container database độc lập gồm SQL Server 2022 (port 1433), MongoDB 7.0.5 (port 27017) và MySQL 8.3.0 (port 3306) cùng container hỗ trợ sqlserver-init. Lệnh 'docker compose ps' xác nhận tất cả container đều ở trạng thái running (Up/Healthy), sẵn sàng phục vụ các microservice.",
        "commit": "chore(infra): add docker compose for sql server, mongodb and mysql"
    },
    "0.2": {
        "title": "TODO 0.2 Script tạo database (sqlserver/init.sql & mysql/init.sql)",
        "result": "Container cinema-sqlserver-init chạy script sqlserver/init.sql thành công (exit 0) tạo database cinema_customer trên SQL Server. Script mysql/init.sql tạo database cinema_booking và cấp quyền cho root trên MySQL. Dữ liệu và database được tạo tự động ngay khi Docker khởi động mà không cần thao tác tay.",
        "commit": "chore(infra): add init scripts for sql server and mysql databases"
    },
    "0.3": {
        "title": "TODO 0.3 Bootstrap 3 microservices (customer-service, movie-service, booking-service)",
        "result": "Khởi tạo thành công khung dự án Spring Boot (Java 21) cho cả 3 microservice backend. File pom.xml của từng service được nạp đầy đủ các dependency (SQL Server driver + Flyway cho customer; Spring Data MongoDB cho movie; MySQL driver + Flyway cho booking). Lệnh 'mvn compile' cho cả 3 service đều đạt BUILD SUCCESS, không có lỗi cấu hình.",
        "commit": "build(customer): bootstrap customer-service with sql server driver and flyway\n- build(movie): bootstrap movie-service with spring data mongodb\n- build(booking): bootstrap booking-service with mysql and flyway"
    },
    "0.4": {
        "title": "TODO 0.4 Bootstrap api-gateway",
        "result": "Khởi tạo project api-gateway (port 9000) với Spring Cloud Gateway Server Web MVC và OAuth2 Resource Server. Lệnh 'mvn compile' thành công đạt BUILD SUCCESS, sẵn sàng làm cổng ngõ tập trung bảo vệ và điều hướng hệ thống.",
        "commit": "build(gateway): bootstrap api-gateway with gateway webmvc and resource server"
    },
    "0.5": {
        "title": "TODO 0.5 Cấu hình application.properties cho các service",
        "result": "Cấu hình chuẩn xác thông số cho từng service: customer-service (port 8081, kết nối SQL Server), movie-service (port 8082, kết nối MongoDB URI), booking-service (port 8083, kết nối MySQL và cấu hình URL movie-service). Khởi động từng service kết nối database thành công, không gặp lỗi 'Connection refused'.",
        "commit": "chore(customer): configure sql server datasource and jpa settings\n- chore(movie): configure mongodb connection uri and auto index creation\n- chore(booking): configure port, datasource and movie service url"
    },
    "0.6": {
        "title": "TODO 0.6 Xử lý ngoại lệ dùng chung (GlobalExceptionHandler)",
        "result": "Định nghĩa class @RestControllerAdvice ở cả 3 service để bắt toàn bộ ngoại lệ và chuẩn hóa cấu trúc JSON trả về: { timestamp, status, error, message, path }. Khi gửi request sai URL hoặc dữ liệu không hợp lệ, hệ thống trả về đúng mã lỗi (400, 404, 500) kèm format JSON chuẩn thay vì trang lỗi mặc định của Spring.",
        "commit": "feat(customer): add global exception handler with unified error body\n- feat(movie): add global exception handler with unified error body\n- feat(booking): add global exception handler with unified error body"
    },
    "1.1": {
        "title": "TODO 1.1 Cấu hình tài khoản Admin & JWT properties",
        "result": "Cấu hình tài khoản Admin cố định (admin@fucinema.com / @@abc123@@) và secret key JWT HS256 (độ dài >= 32 ký tự), thời hạn token trong application.properties của customer-service, sẵn sàng cho việc xác thực và phân quyền.",
        "commit": "chore(customer): configure admin account and jwt properties"
    },
    "1.2": {
        "title": "TODO 1.2 Cấu hình BCryptPasswordEncoder Bean",
        "result": "Đăng ký Bean BCryptPasswordEncoder vào Spring Context. Mật khẩu khách hàng khi đăng ký hoặc đổi mật khẩu đều được băm một chiều thành chuỗi $2a$..., đảm bảo an toàn tuyệt đối và không lưu mật khẩu thô trong SQL Server.",
        "commit": "feat(customer): add bcrypt password encoder bean"
    },
    "1.3": {
        "title": "TODO 1.3 Cài đặt JwtService ký token HS256",
        "result": "JwtService sinh access token JWT chuẩn HS256 với cấu trúc 3 phần (header.payload.signature), nhúng đầy đủ các claims: subject (email), uid (ID người dùng) và role (ADMIN hoặc CUSTOMER) phục vụ Gateway bóc tách context.",
        "commit": "feat(customer): add JwtService to sign HS256 access tokens"
    },
    "1.4": {
        "title": "TODO 1.4 Triển khai login cho Admin và Customer (AuthService)",
        "result": "AuthService kiểm tra đăng nhập chuẩn xác: Admin so khớp trực tiếp thông tin cấu hình; Customer so khớp hash BCrypt trong database và chặn nếu trạng thái tài khoản là INACTIVE (trả về 403 Forbidden). Đăng nhập thành công trả về access token.",
        "commit": "feat(customer): implement login for admin and customers"
    },
    "1.5": {
        "title": "TODO 1.5 Mở API POST /api/auth/login",
        "result": "Postman kiểm thử POST /api/auth/login: Đăng nhập đúng trả về 200 OK kèm accessToken; Đăng nhập sai mật khẩu trả về 401 Unauthorized; Đăng nhập tài khoản Chi (bị INACTIVE) trả về 403 Forbidden đúng theo nghiệp vụ.",
        "commit": "feat(customer): expose POST /api/auth/login"
    },
    "2.1": {
        "title": "TODO 2.1 Flyway migration tạo bảng customer trên SQL Server",
        "result": "Script V1__init_customer.sql chạy qua Flyway tạo bảng customer với kiểu NVARCHAR hỗ trợ tiếng Việt có dấu, UNIQUE email và nạp sẵn 3 khách hàng mẫu (An, Bình: ACTIVE; Chi: INACTIVE).",
        "commit": "feat(customer): add t-sql migrations with nvarchar and unicode seed data"
    },
    "2.2": {
        "title": "TODO 2.2 Tạo Customer Entity & CustomerRepository",
        "result": "Entity Customer ánh xạ chính xác vào bảng customer trong SQL Server. CustomerRepository kế thừa JpaRepository cung cấp sẵn các phương thức tìm kiếm findByEmail và existsByEmail hoạt động trơn tru.",
        "commit": "feat(customer): add Customer entity and repository"
    },
    "2.3": {
        "title": "TODO 2.3 Tạo DTOs kèm Validation",
        "result": "Các DTO (RegisterRequest, UpdateProfileRequest, ChangePasswordRequest, CustomerResponse) được định nghĩa đầy đủ với annotation kiểm tra hợp lệ (@NotBlank, @Email, @Past). Dữ liệu sai sẽ bị bắt lỗi ngay từ tầng Controller.",
        "commit": "feat(customer): add register, profile and password DTOs with validation"
    },
    "2.4": {
        "title": "TODO 2.4 Triển khai đăng ký khách hàng (CustomerService.register)",
        "result": "Postman test POST /api/auth/register: Đăng ký thành công trả về 201 Created kèm thông tin tài khoản (ẩn password); Đăng ký trùng email lập tức bị chặn với mã 400 Bad Request.",
        "commit": "feat(customer): implement customer registration with unique email"
    },
    "2.5": {
        "title": "TODO 2.5 Triển khai xem, sửa hồ sơ & đổi mật khẩu",
        "result": "Khách hàng có thể lấy thông tin cá nhân theo ID, cập nhật thông tin và đổi mật khẩu. Đổi mật khẩu kiểm tra đúng mật khẩu cũ mới cho phép đổi, tránh lộ thông tin và đổi trái phép.",
        "commit": "feat(customer): implement view, update profile and change password"
    },
    "2.6": {
        "title": "TODO 2.6 Mở các endpoints /me",
        "result": "Postman test: GET /api/customers/me trả về 200 OK với thông tin người dùng từ header X-User-Id; PUT /api/customers/me cập nhật thành công; PUT /api/customers/me/password đổi mật khẩu thành công.",
        "commit": "feat(customer): expose register and /me endpoints"
    },
    "3.1": {
        "title": "TODO 3.1 Tạo DTO AdminCustomerRequest",
        "result": "DTO AdminCustomerRequest được bổ sung trường status (ACTIVE/INACTIVE), cho phép Admin quản lý toàn diện thông tin và trạng thái kích hoạt của khách hàng.",
        "commit": "feat(customer): add AdminCustomerRequest DTO"
    },
    "3.2": {
        "title": "TODO 3.2 Triển khai tìm kiếm & CRUD với Soft Delete cho Admin",
        "result": "Admin tìm kiếm khách hàng theo từ khóa kết hợp phân trang và sắp xếp. Khi xóa khách hàng, hệ thống thực hiện xóa mềm (chuyển status = INACTIVE) giúp bảo toàn dữ liệu lịch sử đặt vé.",
        "commit": "feat(customer): implement admin customer search and crud with soft delete"
    },
    "3.3": {
        "title": "TODO 3.3 Mở endpoints quản trị khách hàng cho Admin",
        "result": "Postman test: GET /api/customers trả về danh sách khách hàng có phân trang (200 OK); DELETE /api/customers/{id} vô hiệu hóa tài khoản thành công, kiểm tra lại DB trạng thái chuyển thành INACTIVE.",
        "commit": "feat(customer): expose admin customer crud endpoints"
    },
    "4.1": {
        "title": "TODO 4.1 Tạo DataSeeder nạp dữ liệu mẫu vào MongoDB",
        "result": "Khi movie-service khởi động, DataSeeder tự động kiểm tra và nạp dữ liệu mẫu vào các collection genres, cinema_rooms, movies, showtimes. Mở MongoDB Compass kiểm tra thấy dữ liệu được tạo đầy đủ với ID dạng ObjectId.",
        "commit": "feat(movie): add DataSeeder for genres, rooms, movies and showtimes"
    },
    "4.2": {
        "title": "TODO 4.2 Tạo Document & Repository cho Genre và CinemaRoom",
        "result": "Document Genre và CinemaRoom được đánh chỉ mục duy nhất (@Indexed(unique = true)) trên genreName và roomName, ngăn chặn tạo trùng lặp thể loại hoặc phòng chiếu.",
        "commit": "feat(movie): add Genre and CinemaRoom documents with unique indexes"
    },
    "4.3": {
        "title": "TODO 4.3 Triển khai GenreService & RoomService (Ràng buộc BR03)",
        "result": "Thực hiện CRUD thể loại và phòng chiếu. Ràng buộc BR03 hoạt động chuẩn xác: trước khi xóa thể loại, service kiểm tra nếu có phim đang thuộc thể loại đó thì chặn lại và trả về lỗi 400 Bad Request.",
        "commit": "feat(movie): implement genre and room services with delete guards"
    },
    "4.4": {
        "title": "TODO 4.4 Mở endpoints Genre & Room",
        "result": "Postman test: GET /api/genres và GET /api/rooms trả về danh sách dữ liệu mẫu (200 OK); Thử xóa thể loại đang có phim bị chặn với lỗi 400 đúng quy tắc BR03.",
        "commit": "feat(movie): expose genre and room endpoints"
    },
    "5.1": {
        "title": "TODO 5.1 Tạo Document Movie & các Enum",
        "result": "Document Movie lưu trữ đầy đủ thông tin phim, lưu genreId dạng String, tích hợp các Enum AgeRating và MovieStatus trên MongoDB.",
        "commit": "feat(movie): add Movie document referencing genre id"
    },
    "5.2": {
        "title": "TODO 5.2 Tìm kiếm phim động bằng MongoTemplate",
        "result": "API tìm kiếm phim lọc linh hoạt theo tiêu đề (không phân biệt hoa thường), lọc theo thể loại (genreId), theo trạng thái (status) kết hợp phân trang và sắp xếp chính xác.",
        "commit": "feat(movie): search movies with MongoTemplate criteria"
    },
    "5.3": {
        "title": "TODO 5.3 Triển khai MovieService CRUD (Kiểm tra BR15)",
        "result": "MovieService kiểm tra thủ công sự tồn tại của genreId trong collection genres trước khi thêm/sửa phim (BR15 do MongoDB không có FK). Truyền genreId sai bị báo lỗi 400 Bad Request.",
        "commit": "feat(movie): implement movie crud with genre existence check"
    },
    "5.4": {
        "title": "TODO 5.4 Mở endpoints cho Movie",
        "result": "Postman test: Xem danh sách phim công khai GET /api/movies và chi tiết GET /api/movies/{id} (200 OK); Admin thêm mới phim thành công với mã 201 Created.",
        "commit": "feat(movie): expose movie endpoints"
    },
    "6.1": {
        "title": "TODO 6.1 Tạo Document Showtime với giá Decimal128",
        "result": "Document Showtime được định nghĩa với trường giá vé ticketPrice lưu dưới dạng Decimal128 trong MongoDB để tránh sai số tiền tệ, cùng các trường thời gian bắt đầu, kết thúc, phòng chiếu và phim.",
        "commit": "feat(movie): add Showtime document with decimal128 price"
    },
    "6.2": {
        "title": "TODO 6.2 Query kiểm tra trùng lịch chiếu",
        "result": "Derived query trong ShowtimeRepository kiểm tra các suất chiếu SCHEDULED trong cùng một phòng bị giao thoa thời gian (startTime < newEnd && endTime > newStart).",
        "commit": "feat(movie): add derived query counting overlapping showtimes"
    },
    "6.3": {
        "title": "TODO 6.3 Triển khai logic tạo suất chiếu (BR04, BR05)",
        "result": "Tự động tính endTime = startTime + movie.duration (BR04). Khi tạo suất chiếu bị đè lịch lên suất chiếu có sẵn trong cùng phòng chiếu, hệ thống chặn lại và báo lỗi 400 Bad Request (BR05).",
        "commit": "feat(movie): validate and schedule showtimes with computed end time"
    },
    "6.4": {
        "title": "TODO 6.4 Hủy suất chiếu (BR06) & tìm kiếm suất chiếu theo ngày",
        "result": "Hủy suất chiếu thành công với PUT /api/showtimes/{id}/cancel chuyển trạng thái sang CANCELLED (BR06). Danh sách suất chiếu được lọc chính xác theo ngày chiếu và phim.",
        "commit": "feat(movie): implement showtime cancel and search by movie and date"
    },
    "6.5": {
        "title": "TODO 6.5 Mở endpoints Showtime",
        "result": "Postman test: GET /api/showtimes/{id} trả về chi tiết thông tin suất chiếu (200 OK) phục vụ cho Booking Service gọi OpenFeign sang.",
        "commit": "feat(movie): expose showtime endpoints"
    },
    "7.1": {
        "title": "TODO 7.1 Thêm OpenFeign & Spring Cloud BOM vào booking-service",
        "result": "File pom.xml của booking-service tích hợp OpenFeign thành công. Class chính được gắn @EnableFeignClients, biên dịch 'mvn compile' đạt BUILD SUCCESS.",
        "commit": "build(booking): add openfeign and spring cloud bom"
    },
    "7.2": {
        "title": "TODO 7.2 Flyway migration tạo bảng bookings và booking_details trên MySQL",
        "result": "Migration V1__init_booking.sql tạo 2 bảng bookings và booking_details trên MySQL. Các cột showtime_id, movie_id được đặt kiểu VARCHAR(24) để chứa vừa ObjectId của MongoDB.",
        "commit": "feat(booking): add mysql migration with varchar object id columns"
    },
    "7.3": {
        "title": "TODO 7.3 Tạo Entity Booking & BookingDetail",
        "result": "Hai Entity JPA được thiết lập quan hệ 1-N với cascade = CascadeType.ALL và orphanRemoval = true, đảm bảo lưu hóa đơn và danh sách vé trong cùng một transaction ACID.",
        "commit": "feat(booking): add Booking and BookingDetail entities"
    },
    "7.4": {
        "title": "TODO 7.4 Tạo MovieClient (OpenFeign)",
        "result": "Interface MovieClient gọi trực tiếp sang movie-service:8082 lấy thông tin suất chiếu thành công thông qua REST nội bộ.",
        "commit": "feat(booking): add MovieClient feign client with string showtime id"
    },
    "7.5": {
        "title": "TODO 7.5 Triển khai logic đặt vé (BookingService.createBooking)",
        "result": "Logic đặt vé kiểm tra toàn diện: validate ghế không trùng lặp (BR07), ghế hợp lệ theo sơ đồ phòng (BR08), ghế chưa có ai đặt (BR09). Tự động tính tiền trên server và chụp snapshot phim/phòng. Đặt vé thành công trả về 201 Created; đặt trùng ghế báo lỗi 400 Bad Request.",
        "commit": "feat(booking): implement booking creation with seat validation"
    },
    "7.6": {
        "title": "TODO 7.6 Triển khai sơ đồ ghế suất chiếu (getSeatMap)",
        "result": "Postman test GET /api/showtimes/{id}/seats trả về sơ đồ toàn bộ ghế của phòng chiếu, đánh dấu chính xác ghế đã đặt là BOOKED và ghế còn trống là AVAILABLE.",
        "commit": "feat(booking): add seat map for a showtime"
    },
    "7.7": {
        "title": "TODO 7.7 Mở endpoints đặt vé & sơ đồ ghế",
        "result": "Các API POST /api/bookings và GET /api/showtimes/{id}/seats hoạt động ổn định và chính xác trên Postman.",
        "commit": "feat(booking): expose create booking and seat map endpoints"
    },
    "8.1": {
        "title": "TODO 8.1 Lịch sử đặt vé khách hàng (getMyBookings)",
        "result": "Khách hàng gọi GET /api/bookings/my nhận danh sách các đơn vé của chính mình theo X-User-Id, sắp xếp theo thứ tự ngày đặt mới nhất lên đầu (createdAt DESC).",
        "commit": "feat(booking): add customer booking history sorted by date"
    },
    "8.2": {
        "title": "TODO 8.2 Xem chi tiết vé & phân quyền (BR11)",
        "result": "API kiểm tra quyền truy cập BR11: khách hàng xem đơn vé của mình trả về 200 OK; xem vé của người khác bị chặn với mã 403 Forbidden. Admin có quyền xem tất cả đơn vé.",
        "commit": "feat(booking): restrict booking detail to owner or admin"
    },
    "8.3": {
        "title": "TODO 8.3 Hủy vé & giải phóng ghế (BR12)",
        "result": "Quy tắc BR12 được áp dụng: chỉ cho phép hủy vé trước giờ chiếu ít nhất 2 tiếng. Khi hủy thành công (200 OK), trạng thái vé chuyển sang CANCELLED và ghế lập tức được giải phóng trở lại AVAILABLE.",
        "commit": "feat(booking): allow cancelling bookings 2 hours before showtime"
    },
    "8.4": {
        "title": "TODO 8.4 Mở endpoints xem lịch sử, chi tiết & hủy vé",
        "result": "Toàn bộ các API GET /api/bookings/my, GET /api/bookings/{id}, PUT /api/bookings/{id}/cancel và GET /api/bookings (cho Admin) được mở đầy đủ và hoạt động chuẩn xác.",
        "commit": "feat(booking): expose history, detail, cancel and admin list endpoints"
    },
    "9.1": {
        "title": "TODO 9.1 Viết truy vấn báo cáo doanh thu theo khoảng ngày",
        "result": "Query trong BookingRepository nhóm theo từng bộ phim và tính tổng số vé, tổng doanh thu của các đơn vé hợp lệ (CONFIRMED) trong khoảng thời gian chỉ định.",
        "commit": "feat(booking): add report query by booking date range"
    },
    "9.2": {
        "title": "TODO 9.2 Triển khai logic báo cáo doanh thu (BR13)",
        "result": "Báo cáo doanh thu được tính toán và sắp xếp giảm dần theo doanh thu (phim có doanh thu cao nhất đứng đầu - BR13), kèm theo tổng doanh thu toàn hệ thống.",
        "commit": "feat(booking): implement revenue report sorted descending"
    },
    "9.3": {
        "title": "TODO 9.3 Mở endpoint GET /api/bookings/report",
        "result": "API báo cáo doanh thu: Admin gọi trả về 200 OK kèm bảng số liệu thống kê chi tiết; Customer gọi bị từ chối với mã 403 Forbidden.",
        "commit": "feat(booking): expose GET /api/bookings/report"
    },
    "10.1": {
        "title": "TODO 10.1 Cấu hình Gateway (application.properties)",
        "result": "Cấu hình api-gateway port 9000, trỏ URL tới 3 backend service và cấu hình chung secret key JWT HS256 đồng bộ với Customer Service.",
        "commit": "chore(gateway): configure service urls and jwt secret"
    },
    "10.2": {
        "title": "TODO 10.2 Viết UserHeaderFilter bóc tách context người dùng",
        "result": "UserHeaderFilter giải mã JWT token, loại bỏ các header X-User-* giả mạo từ client và chèn lại các header chuẩn xác (X-User-Id, X-User-Email, X-User-Role) chuyển tiếp cho backend.",
        "commit": "feat(gateway): forward user context headers from jwt"
    },
    "10.3": {
        "title": "TODO 10.3 Cấu hình định tuyến (Routes.java)",
        "result": "Router định tuyến chính xác: /api/auth/** và /api/customers/** tới customer-service; /api/movies/**, /api/genres/**, /api/rooms/**, /api/showtimes/** tới movie-service; /api/bookings/** tới booking-service.",
        "commit": "feat(gateway): add routes for customer, movie and booking services"
    },
    "10.4": {
        "title": "TODO 10.4 Phân quyền & bảo mật (SecurityConfig)",
        "result": "SecurityConfig kiểm soát an ninh toàn diện: các API công khai truy cập không cần token; API yêu cầu role CUSTOMER hoặc ADMIN được kiểm tra chính xác. Không có token báo 401; sai role báo 403.",
        "commit": "feat(gateway): secure endpoints with jwt and role-based rules"
    },
    "11.1": {
        "title": "TODO 11.1 Tạo Postman Environment",
        "result": "Environment FUCinema_Local được thiết lập với base_url = http://localhost:9000 và các biến lưu trữ tự động token của Admin và Customer.",
        "commit": "test(postman): add local environment"
    },
    "11.2": {
        "title": "TODO 11.2 Tạo Postman Collection kiểm thử F1 - F10",
        "result": "Toàn bộ kịch bản kiểm thử từ F1 đến F10 được tổ chức bài bản trong Collection, có gắn các test script tự động kiểm tra status code và dữ liệu JSON trả về.",
        "commit": "test(postman): add collection with test scripts for F1-F10"
    },
    "11.3": {
        "title": "TODO 11.3 Chạy Collection Runner & hoàn thiện bài nộp",
        "result": "Chạy Collection Runner trong Postman: toàn bộ tất cả các test case đều vượt qua với kết quả Pass 100% (màu xanh lá, 0 Fail), chứng minh hệ thống hoạt động hoàn hảo.",
        "commit": "docs: add run guide and test accounts to README"
    }
}

def insert_p_after(para, bold_prefix, text):
    new_p = OxmlElement('w:p')
    para._p.addnext(new_p)
    new_para = Paragraph(new_p, para._parent)
    run_b = new_para.add_run(bold_prefix)
    run_b.bold = True
    run_t = new_para.add_run(text)
    return new_para

def main():
    doc = docx.Document('Assignment 1_DE190685_ManhLV.docx')
    
    # 1. First, detect TODO sections and their last image
    todos = []
    current_todo = None

    for i, p in enumerate(doc.paragraphs):
        text = p.text.strip()
        drawings = len(p._p.xpath('.//w:drawing'))
        is_toc = any(text.startswith(f"{x}.") for x in range(1, 15))
        if 'TODO ' in text and not is_toc:
            if current_todo:
                todos.append(current_todo)
            current_todo = {
                'header_para': p,
                'header_text': text,
                'last_img_para': None,
            }
        elif current_todo:
            if drawings > 0:
                current_todo['last_img_para'] = p

    if current_todo:
        todos.append(current_todo)

    print(f"Detected {len(todos)} TODOs.")

    # 2. Iterate and enrich each TODO
    updated_count = 0
    for t in todos:
        header_text = t['header_text']
        # Find key in DATA (e.g. '0.1', '1.4', etc.)
        matched_key = None
        for key in DATA:
            if f"TODO {key}" in header_text:
                matched_key = key
                break
        
        if not matched_key:
            print(f"Warning: No data for {header_text}")
            continue

        item = DATA[matched_key]
        
        # Update header title if it is just bare 'TODO X.Y'
        if header_text.strip() == f"TODO {matched_key}":
            t['header_para'].text = item['title']
            t['header_para'].runs[0].bold = True
        
        # Insert explanation after last image
        target_para = t['last_img_para']
        if not target_para:
            target_para = t['header_para']
        
        # Insert explanation and commit
        p_res = insert_p_after(target_para, "Kết quả chạy: ", item['result'])
        p_com = insert_p_after(p_res, "Commit: ", item['commit'])
        
        # Add a blank spacing paragraph
        empty_p = OxmlElement('w:p')
        p_com._p.addnext(empty_p)
        
        updated_count += 1

    output_filename = 'Assignment 1_DE190685_ManhLV_Updated.docx'
    doc.save(output_filename)
    print(f"Successfully updated and saved {updated_count} TODO sections in {output_filename}!")

if __name__ == '__main__':
    main()
