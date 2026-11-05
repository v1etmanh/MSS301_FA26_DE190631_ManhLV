package com.mss301.brand.dto;

// [TODO-5.4: kết quả gán / gỡ watch. status: ASSIGNED | UNASSIGNED | NOTHING_TO_DO]
public record AssignmentResponse(Integer watchId, Integer brandId, Integer previousBrandId, String status) {
}
