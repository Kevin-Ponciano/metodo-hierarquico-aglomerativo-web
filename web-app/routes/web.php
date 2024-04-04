<?php

use App\Livewire\App;
use Illuminate\Support\Facades\Route;

Route::get('/', App::class);

Route::post('/upload', [App::class, 'upload'])->name('upload');
