import { Injectable } from '@angular/core';
import { Http, Headers, Response } from '@angular/http';
import { Observable } from 'rxjs';
import { AlertService } from './alert.service';
import 'rxjs/add/operator/map'

@Injectable()
export class AuthenticationService {
    public token: string;
    public apiUrl: string;
    constructor(private http: Http, private alertService: AlertService) {
        // set token if saved in local storage
        var currentUser = JSON.parse(localStorage.getItem('currentUser'));
        this.token = currentUser && currentUser.token;
         this.apiUrl='/api';
    }

    login(username: string, password: string): Observable<Response> {
        return this.http.post(this.apiUrl+'/login', JSON.stringify({ username: username, password: password }))
            .map((response: Response) => {
                return response;
            });
    }

    
    logout(): void {
        // clear token remove user from local storage to log user out
        this.token = null;
        localStorage.removeItem('currentUser');
    }
}