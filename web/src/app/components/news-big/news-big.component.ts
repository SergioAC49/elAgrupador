import { Component, OnInit, Input } from '@angular/core';
import { News } from '../../classes/news';

@Component({
  selector: 'app-news-big',
  templateUrl: './news-big.component.html',
  styleUrls: ['./news-big.component.css']
})
export class NewsBigComponent implements OnInit {

	@Input() news: News;
	
	constructor() {
	}

	ngOnInit(): void {
		console.log(this.news);
	}

}