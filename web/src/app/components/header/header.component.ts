import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl, Validators } from '@angular/forms';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {

	control: FormControl = new FormControl('');

	constructor() {
		this.control.valueChanges
			.subscribe(value => {
				console.log(value);
			});
	}

	ngOnInit(): void { }

	search(value: string) {
		console.log("Search: ", value);
	}

}
