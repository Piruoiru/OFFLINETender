<?php

namespace App\Filament\Pages;

use Filament\Pages\Page;

class ChatPage extends Page
{
    protected static ?string $navigationIcon = 'heroicon-o-chat-bubble-left-right';

    protected static string $view = 'filament.pages.chat-page';

    protected static ?string $title = 'Chat Assistant';

    protected static ?string $navigationLabel = 'Chat Assistant';

    protected static ?string $navigationGroup = 'ChatAI Assistant';
}
