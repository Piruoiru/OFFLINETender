<?php

namespace App\Providers;

use Illuminate\Support\ServiceProvider;
use Livewire\Livewire;
use App\Livewire\ChatAssistant;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        $this->app->bind(
            \App\Repositories\Contracts\MessageRepositoryInterface::class,
            \App\Repositories\MessageRepository::class
        );

        $this->app->bind(
            \App\Repositories\Contracts\ConversationRepositoryInterface::class,
            \App\Repositories\ConversationRepository::class
        );
    }

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Livewire::component('chat-assistant', ChatAssistant::class);
    }
}
