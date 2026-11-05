package com.mss301.watch.repository;

import com.mss301.watch.entity.Watch;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

// [TODO-6.16: watch mới nhất (WatchID lớn nhất) ở đầu danh sách]
public interface WatchRepository extends JpaRepository<Watch, Integer> {

    List<Watch> findAllByOrderByWatchIdDesc();
}
