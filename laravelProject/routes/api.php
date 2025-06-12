<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\{
    ConversationController,
    MessageController,
    MessageStreamController
};

Route::prefix('conversations')->group(function () {
    Route::get('/',  [ConversationController::class, 'index']);
    Route::post('/', [ConversationController::class, 'storeConversation']);

    // ——— MESSAGGI (mettili prima) ———
    Route::get('{conversation}/messages',  [MessageController::class, 'index']);
    Route::post('{conversation}/messages', [MessageController::class, 'storeMessage']);

    Route::get('{conversation}/stream', MessageStreamController::class);

    // —— SHOW va in coda, è la meno specifica ——
    Route::get('{conversation}', [ConversationController::class, 'show']);
});


// DA TESTARE MODIFICARE LA ROBA PER CREARE CONVERSAZIONE DARE A CHAT IL MIO FILE CON LA TABELLA DELLA CONVERSAZIONE E FARGLIELA RICRRARE L'API 