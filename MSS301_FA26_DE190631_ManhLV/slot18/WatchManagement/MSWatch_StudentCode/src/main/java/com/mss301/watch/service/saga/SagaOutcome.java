package com.mss301.watch.service.saga;

/** Kết quả một Saga chạy xong: id Saga, WatchID liên quan, trạng thái cuối. */
// [TODO-6.9]
public record SagaOutcome(String sagaId, Integer watchId, SagaStatus status) {
}
