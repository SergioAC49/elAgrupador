import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';

import { MatCardModule } from '@angular/material/card';
import { MatGridListModule } from '@angular/material/grid-list';
import { MatToolbarModule } from '@angular/material/toolbar';  
import { MatIconModule } from '@angular/material/icon';    

import { NgMatSearchBarModule } from 'ng-mat-search-bar';

import { AppComponent } from './app.component';
import { MyComponent } from './components/my-component/my-component.component';
import { MainComponent } from './components/main/main.component';
import { NewsBigComponent } from './components/news-big/news-big.component';
import { NewsMediumComponent } from './components/news-medium/news-medium.component';
import { NewsSmallComponent } from './components/news-small/news-small.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HeaderComponent } from './components/header/header.component';
import { SearchResultComponent } from './components/search-result/search-result.component';
import { SimilarNewsComponent } from './components/similar-news/similar-news.component';
import { ArticleDetailsComponent } from './components/article-details/article-details.component';

@NgModule({
  declarations: [
    AppComponent, 
    MyComponent, 
    MainComponent, 
    NewsBigComponent, NewsMediumComponent, NewsSmallComponent, HeaderComponent, SearchResultComponent, SimilarNewsComponent, ArticleDetailsComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule, 
    HttpClientModule, 
    MatCardModule, 
    MatGridListModule, 
    MatToolbarModule, 
    MatIconModule, 
    NgMatSearchBarModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
