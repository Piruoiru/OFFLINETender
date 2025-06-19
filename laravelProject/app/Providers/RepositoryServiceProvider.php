<?php

namespace App\Providers;

use Illuminate\Foundation\Support\Providers\RouteServiceProvider as ServiceProvider;
use App\Repositories\Contracts\MessageRepositoryInterface;
use App\Repositories\MessageRepository;
use App\Repositories\Contracts\ConversationRepositoryInterface;
use App\Repositories\ConversationRepository;

class RepositoryServiceProvider extends ServiceProvider
{
   public function register(): void
   {
    $this->app->bind(MessageRepositoryInterface::class, MessageRepository::class);
    $this->app->bind(ConversationRepositoryInterface::class, ConversationRepository::class);
   }
}
