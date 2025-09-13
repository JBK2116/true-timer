package com.jbk.trueTimer.controllers;

import com.jbk.trueTimer.dto.UserCreationDTO;
import com.jbk.trueTimer.services.PublicUserService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.ExampleObject;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/users")
@Tag(name = "User Management", description = "Operations for managing users")

public class PublicUserController {

    private final PublicUserService publicUserService;

    @Autowired
    public PublicUserController(PublicUserService publicUserService) {
        this.publicUserService = publicUserService;
    }

    @PostMapping("")
    @Operation(summary = "Create User", description = "Create a user and return their unique token")
    @ApiResponses(value = {
            @ApiResponse(responseCode = "201", description = "User Created",
                    content = @Content(examples = {@ExampleObject(value = "{\"token\": \"f47ac10b-58cc-4372-a567-0e02b2c3d479Retry\"}")})),
            @ApiResponse(responseCode = "400", description = "Bad Request",
                    content = @Content(examples = {@ExampleObject(value = "{'field name': 'error message'}")}))})
    public ResponseEntity<Void> createUser(@Valid @RequestBody UserCreationDTO dto) {
        System.out.println(dto.toString());
        return ResponseEntity.status(HttpStatus.CREATED).build();
    }
}
