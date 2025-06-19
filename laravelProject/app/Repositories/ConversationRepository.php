<?php


namespace App\Repositories;


use App\Models\Conversation;
use App\Repositories\Contracts\ConversationRepositoryInterface;
use App\Utils\OaRepository;


class ConversationRepository implements ConversationRepositoryInterface
{
   public function store(
       array $conversation
   ): Conversation
   {

    logger()->info('Auth check', [
        'guard'   => auth()->guard()->getName(),
        'check'   => auth()->check(),
        'id'      => auth()->id(),
        'cookies' => request()->cookies->keys(),
        'headers' => [
            'cookie'  => request()->header('cookie'),
            'auth'    => request()->header('authorization'),
            'referer' => request()->header('referer'),
        ],
    ]);

       $new_conversation = new Conversation();

       $new_conversation->title = OaRepository::store($conversation, 'title');
    //    $new_conversation->user_id = (OaRepository::store($conversation, 'user_id')?? auth()->id());
       $new_conversation->user_id = OaRepository::store($conversation, 'user_id') ?: 1;

       $new_conversation->save();


       return $new_conversation;
   }


   public function update(
       int $conversation_id,
       array $conversation
   ): Conversation
   {
       $db_conversation = Conversation::find($conversation_id);

       $db_conversation->title = OaRepository::update($conversation, 'title', $db_conversation);
       $db_conversation->user_id = (OaRepository::update($conversation, 'user_id', $db_conversation)?? $db_conversation->user_id);

       $db_conversation->save();


       return $db_conversation;
   }
}
