<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\ConversationController;

Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');

Route::get('/conversations', [ConversationController::class, 'conversations']);
Route::get('/conversations/{id}/messages', [ConversationController::class, 'messages']);
Route::post('/conversations/{id}/messages', [ConversationController::class, 'storeMessage']);