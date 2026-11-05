package com.mss301.watch.service;

/** Kết quả trả cho controller: id của Saga vừa chạy (header X-Saga-Id) + dữ liệu response. */
// [TODO-6.14]
public record SagaResult<T>(String sagaId, T body) {
}
