package com.jbk.trueTimer.dto;


import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

import java.util.UUID;

public class UserCreationDTO {
    @NotNull(message = "Timezone must not be empty")
    @Size(min = 1, max = 32, message = "Timezone length must be between 1 and 32 inclusive")
    private final String timezone;

    private final String token;

    @JsonCreator
    public UserCreationDTO(@JsonProperty("timezone") String timezone) {
        this.timezone = timezone;
        this.token = UUID.randomUUID().toString();
    }

    public String toString() {
        return ("Timezone: " + this.timezone + ", Token: " + this.token);
    }
}
