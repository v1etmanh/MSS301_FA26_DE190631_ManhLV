package fu.de190685.post.service.impl;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

import feign.FeignException;
import feign.Request;
import feign.Response;
import fu.de190685.post.client.UserServiceClient;
import fu.de190685.post.common.ApiException;
import fu.de190685.post.dto.ApiResponse;
import fu.de190685.post.dto.PostDTO;
import fu.de190685.post.dto.UserDTO;
import fu.de190685.post.entity.Post;
import fu.de190685.post.repository.PostRepository;
import java.math.BigDecimal;
import java.nio.charset.StandardCharsets;
import java.time.LocalDate;
import java.time.ZoneOffset;
import java.util.Date;
import java.util.Map;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.HttpStatus;

@ExtendWith(MockitoExtension.class)
class PostServiceImplTest {

	@Mock
	private PostRepository postRepository;

	@Mock
	private UserServiceClient userServiceClient;

	@InjectMocks
	private PostServiceImpl postService;

	@Test
	void createCalculatesCostFromRateAndNumberOfDays() {
		UserDTO user = activeUser();
		when(userServiceClient.getUserById(7L)).thenReturn(new ApiResponse<>(1, "Successful", user));
		when(postRepository.save(any(Post.class))).thenAnswer(invocation -> invocation.getArgument(0));

		PostDTO created = postService.create(validPost());

		assertEquals(new BigDecimal("1500000.00"), created.getTotalCost());
		assertEquals("SCHEDULED", created.getStatus());
	}

	@Test
	void createRejectsInactiveUser() {
		UserDTO user = activeUser();
		user.setStatus("DEACTIVATED");
		when(userServiceClient.getUserById(7L)).thenReturn(new ApiResponse<>(1, "Successful", user));

		ApiException exception = assertThrows(ApiException.class, () -> postService.create(validPost()));

		assertEquals(HttpStatus.BAD_REQUEST, exception.getHttpStatus());
		assertEquals(5, exception.getResponseStatus());
	}

	@Test
	void createRejectsPostCountAboveCreatorLimit() {
		UserDTO user = activeUser();
		when(userServiceClient.getUserById(7L)).thenReturn(new ApiResponse<>(1, "Successful", user));
		PostDTO request = validPost();
		request.setNumberOfPosts(4);

		ApiException exception = assertThrows(ApiException.class, () -> postService.create(request));

		assertEquals(HttpStatus.NOT_ACCEPTABLE, exception.getHttpStatus());
		assertEquals(2, exception.getResponseStatus());
	}

	@Test
	void createMapsMissingUserToNotFound() {
		Request request = Request.create(
				Request.HttpMethod.GET,
				"http://localhost:8081/api/users/7",
				Map.of(),
				null,
				StandardCharsets.UTF_8,
				null);
		FeignException notFound = FeignException.errorStatus(
				"UserServiceClient#getUserById", Response.builder().status(404).request(request).build());
		when(userServiceClient.getUserById(7L)).thenThrow(notFound);

		ApiException exception = assertThrows(ApiException.class, () -> postService.create(validPost()));

		assertEquals(HttpStatus.NOT_FOUND, exception.getHttpStatus());
		assertEquals(4, exception.getResponseStatus());
	}

	private UserDTO activeUser() {
		UserDTO user = new UserDTO();
		user.setUserId(7L);
		user.setStatus("ACTIVE");
		user.setRatePerPost(new BigDecimal("500000.00"));
		user.setMaxDailyPosts(3);
		return user;
	}

	private PostDTO validPost() {
		PostDTO post = new PostDTO();
		post.setAdvertiserName("Advertiser");
		post.setAdvertiserEmail("ads@example.com");
		post.setAdvertiserPhone("0123456789");
		post.setStartDate(toDate(LocalDate.of(2026, 7, 1)));
		post.setEndDate(toDate(LocalDate.of(2026, 7, 4)));
		post.setNumberOfPosts(2);
		post.setUserId(7L);
		return post;
	}

	private Date toDate(LocalDate date) {
		return Date.from(date.atStartOfDay().toInstant(ZoneOffset.UTC));
	}
}
