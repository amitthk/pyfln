import { Injectable } from '@angular/core';
import { Http, Headers, RequestOptions, Response } from '@angular/http';
import { Observable } from 'rxjs';
import 'rxjs/add/operator/map'

import { AuthenticationService } from './index';
import { User } from '../models/user';

@Injectable()
export class ProjectService {

    private apiUrl:string;

    constructor(
        private http: Http,
        private authenticationService: AuthenticationService) {
                     this.apiUrl='/api';
    }

    getProjectHome(): Observable<User[]> {

        // get users from api
        return this.http.get(this.apiUrl+'/home', this.jwt())
            .map((response: Response) => response.json());
    }

        private jwt() {
        // create authorization header with jwt token
        let currentUser = JSON.parse(localStorage.getItem('currentUser'));
        if (currentUser && currentUser.token) {
            let headers = new Headers({ 'Authorization': 'Bearer ' + currentUser.token });
            return new RequestOptions({ headers: headers });
        }
    }
}