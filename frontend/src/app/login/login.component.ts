import { Component, Input, OnInit, Output, EventEmitter } from '@angular/core';
import { AuthService } from '../auth-service';
import {FormGroup, FormControl, Validators} from '@angular/forms';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  notFound: boolean = false;

  loginForm = new FormGroup({
    username: new FormControl('', [Validators.required]),
    password: new FormControl('', [Validators.required]),
  });

  @Output() userEmitter = new EventEmitter();

  constructor(private authService: AuthService) {}

  ngOnInit(): void {

  }

  submit(){
    let form = this.loginForm.value;

    this.authService.login(form).subscribe(
      (response: any) => {
        console.log(response.user)
        this.userEmitter.emit(response.user);
      },
      (error: any) => {
        console.log(error.message);
      }
    )
 
  }


  }


