import { Component, OnInit } from '@angular/core';
import { FormControl } from '@angular/forms';
import { Router, ActivatedRoute, ParamMap } from '@angular/router';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {

	control: FormControl = new FormControl('');

	constructor(private router: Router) { }

	ngOnInit(): void { }

	search(value: string) {
		this.router.routeReuseStrategy.shouldReuseRoute = function () { return false; }
	    this.router.onSameUrlNavigation = 'reload';
		this.router.navigate(['/search'], { queryParams: { value: value } });
	}

}
