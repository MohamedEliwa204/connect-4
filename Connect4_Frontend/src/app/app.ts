import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common'; 
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule,FormsModule],
  templateUrl: './app.html',
  styleUrls: ['./app.css']
})
export class AppComponent {
  grid: number[][] = []; 
  gameOver = false;
  winner = '';
  isLoading = false;
  depth : number = 3;
  Ai_Score : number = 0;
  Human_Score : number = 0;

  constructor(private http: HttpClient) {}
  startGame(algo: number) {
    this.Ai_Score = 0;
    this.Human_Score = 0;
    this.isLoading = true;
    this.gameOver = false;
    this.winner = '';
    
    const body = { algo: algo, depth: this.depth };
    
    this.http.post<any>('http://127.0.0.1:5000/start', body).subscribe(res => {
      this.grid = res.grid.reverse();
      this.isLoading = false;
    });
  }

  makeMove(colIndex: number) {
    if (this.gameOver || this.isLoading) return;

    for (let r = this.grid.length - 1; r >= 0; r--) {
      if (this.grid[r][colIndex] === 0) {
        this.grid[r][colIndex] = 1; 
        break;
      }
    }

    this.isLoading = true;
    this.http.post<any>('http://127.0.0.1:5000/move', { col: colIndex }).subscribe(res => {
      this.grid = res.grid.reverse(); 
      if (res.human_score !== undefined) this.Human_Score = res.human_score;
      if (res.ai_score !== undefined) this.Ai_Score = res.ai_score;
      if (res.game_over) {
        this.gameOver = true;
        this.winner = res.winner;
        alert("Game Over! Winner: " + res.winner);
      }
      this.isLoading = false;
    });
  }
  getCellClass(cell: number): string {
    if (cell === 1) return 'player-human';
    if (cell === 2) return 'player-ai';
    return 'empty';
  }
}