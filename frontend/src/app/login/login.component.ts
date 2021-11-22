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
  signup: boolean = false;

  loginForm = new FormGroup({
    username: new FormControl('', [Validators.required]),
    email: new FormControl('', [Validators.email]),
    password: new FormControl('', [Validators.required]),
  });

  @Output() userEmitter = new EventEmitter();

  constructor(private authService: AuthService) {}

  ngOnInit(): void {

  }

  submit(){
    let form = this.loginForm.value;

    if(this.signup) {
      this.authService.signup(form).subscribe(
        (response: any) => {
          this.userEmitter.emit(response);
        },
        (error: any) => {
          console.log(error.message);
        }
      )
    } else {
      this.authService.login(form).subscribe(
        (response: any) => {
          this.userEmitter.emit(response.user);
        },
        (error: any) => {
          console.log(error.message);
        }
      )
    }
 
  }


  }


