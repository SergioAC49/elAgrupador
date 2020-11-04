import { Component, OnInit } from '@angular/core';
import {BreakpointObserver, Breakpoints} from '@angular/cdk/layout';
import { ActivatedRoute } from "@angular/router";

import { NewsService } from '../../services/news.service';
import { Article } from '../../classes/article';

@Component({
  selector: 'app-article',
  templateUrl: './article.component.html',
  styleUrls: ['./article.component.css']
})
export class ArticleComponent implements OnInit {

	public id: string;
	public article: Article;

	constructor(public service: NewsService, breakpointObserver: BreakpointObserver, private route: ActivatedRoute) {

		this.id = this.route.snapshot.paramMap.get("id")

		console.log("ID: ", this.id);

	    this.service.getArticle(this.id).subscribe(data => {
	    	console.log(data);
	    	this.article = data;
	    	console.log("Article: ", this.article);
	    });
	}

	ngOnInit(): void {
		this.id = this.route.snapshot.paramMap.get("id")
	}

}
