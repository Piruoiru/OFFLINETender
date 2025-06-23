<?php


namespace App\Utils;


use Illuminate\Support\Arr;
use Illuminate\Support\Str;
use Webpatser\Uuid\Uuid;


class OaRepository
{
   static public function store(
       array  $request,
       string $key,
       mixed  $default = null
   ): mixed
   {
       return Arr::has($request, $key)
           ? Arr::get($request, $key)
           : $default;
   }


   static public function update(
       array  $request,
       string $key,
       mixed  $db_model
   ): mixed
   {
       return Arr::has($request, $key)
           ? Arr::get($request, $key)
           : $db_model->$key;
   }


   static public function getUniqueUuid(
       ?string $model,
       int     $tryCount = 1
   ): ?string
   {
       $tryCount++;


       if ($tryCount > 10) {
           return null;
       }


       if (is_null($model)) {
           return Uuid::generate(4)->string;
       }


       $uuid = Uuid::generate(4)->string;


       $model = new $model;
       $db_model = $model->where('uuid', $uuid)->first();


       if (!is_null($db_model)) {
           OaRepository::getUniqueUuid($tryCount);
       }


       return $uuid;
   }


   static public function getFileWithExtension(
       string $file_path,
       bool   $is_chunk = false,
       bool   $is_last_chunk = false
   ): string
   {
       if ($is_chunk) {
           $parts = explode('.', pathinfo($file_path, PATHINFO_FILENAME));


           if (count($parts) > 1) {
               array_pop($parts);
           }


           $sanitize_file_name = implode('-', $parts);


           $elements = explode('.', $file_path);


           $extension = $elements[count($elements) - 2];


           if ($is_last_chunk && count($elements) > 2) {
               return Str::slug($sanitize_file_name) . '.' . $extension;
           }


           return count($elements) > 2
               ? Str::slug($sanitize_file_name) . '.' . $elements[count($elements) - 2] . '.' . $elements[count($elements) - 1]
               : Str::slug($sanitize_file_name) . '.' . $elements[count($elements) - 1];
       }


       $file_name_without_extension = pathinfo($file_path, PATHINFO_FILENAME);


       if (Str::contains($file_name_without_extension, '.')) {
           $new_file_name_without_extension = Str::replace('.', '-', $file_name_without_extension);


           return Str::slug($new_file_name_without_extension) . "." . pathinfo($file_path, PATHINFO_EXTENSION);
       }
       return Str::slug($file_name_without_extension) . "." . pathinfo($file_path, PATHINFO_EXTENSION);
   }


   static public function getFileWithoutExtension(
       string $file_path
   ): string
   {
       return pathinfo($file_path, PATHINFO_FILENAME);
   }
}
