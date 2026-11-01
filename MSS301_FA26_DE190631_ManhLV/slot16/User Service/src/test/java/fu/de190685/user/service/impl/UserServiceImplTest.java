package fu.de190685.user.service.impl;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import fu.de190685.user.common.ApiException;
import fu.de190685.user.dto.UserDTO;
import fu.de190685.user.entity.Role;
import fu.de190685.user.entity.User;
import fu.de190685.user.entity.UserStatus;
import fu.de190685.user.repository.UserRepository;
import java.math.BigDecimal;
import java.util.List;
import java.util.Optional;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.PageRequest;
import org.springframework.http.HttpStatus;

@ExtendWith(MockitoExtension.class)
class UserServiceImplTest {

	@Mock
	private UserRepository userRepository;

	@InjectMocks
	private UserServiceImpl userService;

	@Test
	void createSetsActiveStatusByDefault() {
		UserDTO request = validUser();
		when(userRepository.existsByUsername(request.getUsername())).thenReturn(false);
		when(userRepository.save(any(User.class))).thenAnswer(invocation -> invocation.getArgument(0));

		UserDTO created = userService.create(request);

		assertEquals("ACTIVE", created.getStatus());
		assertEquals(request.getUsername(), created.getUsername());
	}

	@Test
	void createRejectsDuplicateUsername() {
		UserDTO request = validUser();
		when(userRepository.existsByUsername(request.getUsername())).thenReturn(true);

		ApiException exception = assertThrows(ApiException.class, () -> userService.create(request));

		assertEquals(HttpStatus.valueOf(226), exception.getHttpStatus());
		assertEquals(3, exception.getResponseStatus());
	}

	@Test
	void updateOnlyChangesProvidedFields() {
		User existing = userEntity();
		when(userRepository.findById(1L)).thenReturn(Optional.of(existing));
		when(userRepository.existsByUsernameAndUserIdNot("new_creator", 1L)).thenReturn(false);
		when(userRepository.save(any(User.class))).thenAnswer(invocation -> invocation.getArgument(0));
		UserDTO update = new UserDTO();
		update.setUsername("new_creator");

		UserDTO result = userService.update(1L, update);

		assertEquals("new_creator", result.getUsername());
		assertEquals("creator@example.com", result.getEmail());
		assertEquals("ACTIVE", result.getStatus());
	}

	@Test
	void getUsersAppliesRoleAndStatusFilters() {
		User user = userEntity();
		when(userRepository.findByRoleAndStatus(Role.CREATOR, UserStatus.ACTIVE, PageRequest.of(0, 10)))
				.thenReturn(new PageImpl<>(List.of(user), PageRequest.of(0, 10), 1));

		userService.getUsers(0, 10, Role.CREATOR, UserStatus.ACTIVE);

		verify(userRepository).findByRoleAndStatus(Role.CREATOR, UserStatus.ACTIVE, PageRequest.of(0, 10));
	}

	private UserDTO validUser() {
		UserDTO user = new UserDTO();
		user.setUsername("creator_a");
		user.setEmail("creator@example.com");
		user.setRole("CREATOR");
		user.setRatePerPost(new BigDecimal("500000.00"));
		user.setMaxDailyPosts(3);
		user.setLevel(1);
		return user;
	}

	private User userEntity() {
		User user = new User();
		user.setUserId(1L);
		user.setUsername("creator_a");
		user.setEmail("creator@example.com");
		user.setRole(Role.CREATOR);
		user.setRatePerPost(new BigDecimal("500000.00"));
		user.setMaxDailyPosts(3);
		user.setLevel(1);
		user.setStatus(UserStatus.ACTIVE);
		return user;
	}
}
