package com.jbk.trueTimer;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.data.jpa.repository.config.EnableJpaAuditing;

@SpringBootApplication
@EnableJpaAuditing
public class TrueTimerApplication {

	public static void main(String[] args) {
		SpringApplication.run(TrueTimerApplication.class, args);
	}

}
