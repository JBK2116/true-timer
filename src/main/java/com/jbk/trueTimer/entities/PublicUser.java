package com.jbk.trueTimer.entities;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Setter
@Getter
@NoArgsConstructor
@Entity
public class PublicUser extends BaseEntity {

    @Column(nullable = false, length = 32)
    private String timezone;

    @Column(nullable = false, length = 36)
    private String token;
}
