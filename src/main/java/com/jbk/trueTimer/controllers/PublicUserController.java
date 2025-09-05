package com.jbk.trueTimer.controllers;

import com.jbk.trueTimer.dto.UserCreationDTO;
import com.jbk.trueTimer.services.PublicUserService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/users")
public class PublicUserController {

    private final PublicUserService publicUserService;

    @Autowired
    public PublicUserController(PublicUserService publicUserService) {
        this.publicUserService = publicUserService;
    }

    @PostMapping("")
    public ResponseEntity<Void> createUser(@Valid @RequestBody UserCreationDTO dto) {
        System.out.println(dto.toString());
        return ResponseEntity.status(HttpStatus.CREATED).build();
    }
}
