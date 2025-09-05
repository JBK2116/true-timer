package com.jbk.trueTimer.repositories;

import com.jbk.trueTimer.entities.PublicUser;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.time.Instant;
import java.util.List;

@Repository
public interface PublicUserRepository extends JpaRepository<PublicUser, Long> {

    PublicUser findByToken(String token);

    List<PublicUser> findAllByCreatedDateBefore(Instant time);
    
}
