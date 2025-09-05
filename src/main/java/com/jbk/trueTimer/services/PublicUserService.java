package com.jbk.trueTimer.services;

import com.jbk.trueTimer.repositories.PublicUserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class PublicUserService {
    private final PublicUserRepository publicUserRepository;

    @Autowired
    public PublicUserService(PublicUserRepository publicUserRepository) {
        this.publicUserRepository = publicUserRepository;
    }

    // Methods Added Below
}
