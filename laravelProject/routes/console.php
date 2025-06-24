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


Schedule::call(fn (ConversationApi $api) => $api->analyze())
        ->dailyAt('00:00')
        ->timezone('Europe/Rome');