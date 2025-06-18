<?php

use Illuminate\Foundation\Inspiring;
use Illuminate\Support\Facades\Artisan;
use Illuminate\Support\Facades\Schedule;
use Illuminate\Support\Facades\Http;
use Illuminate\Http\Request;
use App\Services\ConversationApi;

Artisan::command('inspire', function () {
    $this->comment(Inspiring::quote());
})->purpose('Display an inspiring quote');

// Schedule::call(function () {
//     Log::info('Scheduler /analyze partito');   // debug

//    var_dump(config('services.llm.url'));
//     $response = Http::baseUrl(config('services.llm.url'))   //  ←  http(s)://tuo-sito.test
//     ->acceptJson()
//     ->timeout(30)
//     ->post('/analyze');                   // usa il path reale
    
//     Log::info('Scheduler /analyze terminato', [
//         'status'   => $response->status(),
//         'body'     => $response->body(),          // o ->json()
//     ]);

//     // opzionale: se vuoi che il task fallisca su 4xx/5xx
//     // $response->throw();
// })
// ->dailyAt('14:59')
// ->timezone('Europe/Rome');


Schedule::call(fn (ConversationApi $api) => $api->analyze())
        ->dailyAt('00:00')
        ->timezone('Europe/Rome');