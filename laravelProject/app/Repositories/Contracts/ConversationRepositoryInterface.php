<?php


namespace App\Repositories\Contracts;


use App\Models\Conversation;


interface ConversationRepositoryInterface
{
   public function store(
       array $conversation
   ): Conversation;


   public function update(
       int $conversation_id,
       array $conversation
   ): Conversation;


}
