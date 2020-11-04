import { Component, OnInit } from '@angular/core';
import {BreakpointObserver, Breakpoints} from '@angular/cdk/layout';

import { NewsService } from '../../services/news.service';
import { News } from '../../classes/news';

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.css']
})
export class MainComponent implements OnInit {

	public news: News[];

	public isMobile: boolean = false;

	constructor(public service: NewsService, breakpointObserver: BreakpointObserver) {

		breakpointObserver.observe([
			Breakpoints.Handset
		]).subscribe(result => {
			this.isMobile = result.matches;
		});

	    this.service.getNews().subscribe(data => {
	    	console.log(data);
	    	this.news = data;
	    });
	}

	ngOnInit(): void {}

}
