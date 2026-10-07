# FUCinemaBookingSystem

Assignment 01 implements a cinema ticket booking backend with three microservices and one API Gateway.

## Technology

- Java 21, Spring Boot 4.1.0, Spring Cloud 2025.1.3
- SQL Server 2022 for `customer-service` (port 8081)
- MongoDB 7.0.5 for `movie-service` (port 8082)
- MySQL 8.3.0 for `booking-service` (port 8083)
- Spring Cloud Gateway Server Web MVC (port 9000)
- Flyway, OpenFeign, JWT HS256, BCrypt

## Start the system

Prerequisites: JDK 21, Maven 3.9+, Docker Desktop and Postman Desktop.

From this directory, start the infrastructure and wait until SQL Server is healthy:

```bash
docker compose up -d
docker compose ps -a
```

Then start the applications in this order, one terminal per application:

```bash
mvn -f customer-service/pom.xml spring-boot:run
mvn -f movie-service/pom.xml spring-boot:run
mvn -f booking-service/pom.xml spring-boot:run
mvn -f api-gateway/pom.xml spring-boot:run
```

All client requests must use the gateway at `http://localhost:9000`. Booking Service calls Movie Service directly through OpenFeign.

## Test accounts

| Role | Email | Password | Status |
|---|---|---|---|
| Admin | `admin@fucinema.com` | `@@abc123@@` | Active |
| Customer | `an@gmail.com` | `123456` | Active |
| Customer | `binh@gmail.com` | `123456` | Active |
| Customer | `chi@gmail.com` | `123456` | Inactive (login returns 403) |

## Postman

Import both files from `postman/`:

- `FUCinemaBookingSystem.postman_collection.json`
- `FUCinema-Local.postman_environment.json`

Select `FUCinema-Local`, then run the collection in folder order from `01-Auth` through `08-Report`. The collection contains 85 requests, saves dependent IDs/tokens automatically, and checks the expected response status for every request.

For a deterministic first run, use clean databases. To reset all local assignment data:

```bash
docker compose down -v
```

After stopping the containers, remove the ignored `docker/` bind-mount data directory and start the stack again. Do not commit that directory.

## Useful checks

```bash
curl http://localhost:9000/actuator/health
curl http://localhost:9000/api/movies
```

The JWT secret in `customer-service` and `api-gateway` must remain identical. MongoDB ObjectIds are represented as 24-character strings in API payloads and in the MySQL booking snapshot columns.
