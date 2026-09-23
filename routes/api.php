<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\ImageProcessingController;

Route::post('/process', [ImageProcessingController::class, 'process']);
Route::get('/health', [ImageProcessingController::class, 'health']);
