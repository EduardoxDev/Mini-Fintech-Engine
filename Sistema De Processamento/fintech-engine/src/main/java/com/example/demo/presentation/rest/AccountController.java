package com.example.demo.presentation.rest;
import com.example.demo.core.domain.Account;
import com.example.demo.infrastructure.persistence.AccountRepository;
import org.springframework.web.bind.annotation.*;
import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/api/v1/accounts")
public class AccountController {
    private final AccountRepository accountRepository;
    public AccountController(AccountRepository ar) { this.accountRepository = ar; }

    @PostMapping
    public Account create(@RequestBody Account account) {
        if (account.getId() == null) account.setId(UUID.randomUUID().toString());
        return accountRepository.save(account);
    }

    @GetMapping
    public List<Account> list() {
        return accountRepository.findAll();
    }
}
