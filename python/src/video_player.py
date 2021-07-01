"""A video player class."""

from src.video_playlist import Playlist
from src.video import Video
from .video_library import VideoLibrary
import random
import enum

class video_state(enum.Enum):
    Playing = 1
    Pause = 2
    Stop = 3
    Continue = 4

class vid_stages:
    def __init__(self):
        self.video = None
        self.status = video_state.Stop

    def set_video(self, video, state):
        self.video = video
        self.set_status(state)

    def set_status(self, state):
        self.status = state

        if self.status == video_state.Playing:
            print("Playing video: " + self.video._title)
        elif self.status == video_state.Pause:
            print("Pausing video: " + self.video._title)
        elif self.status == video_state.Stop:
            print("Stopping video: " + self.video._title)
            self.video = None
        elif self.status == video_state.Continue:
            print("Continuing video: " + self.video._title)

class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self): 
        self._video_library = VideoLibrary() 
        self.vid_stages = vid_stages() 

        self.playlists = dict()
        self.userWrittenStylePlaylists = dict()

    # PART 1
    def get_video_details(self, video):

        addition_string = ""
        if video.flagged != None:
            addition_string = " - FLAGGED (reason: " + video.flagged + ")"

        return str(video._title + " (" + video._video_id + ") [" + ' '.join(list(video._tags)) + "]" + addition_string)

    def Sort_video_WRT_Titles(self, videos): 
        videos.sort(key = lambda x: x._title) 
        return videos 

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        # print("show_all_videos needs implementation")
        print("Here's a list of all available videos:")
        for vid in self.Sort_video_WRT_Titles( self._video_library.get_all_videos() ):
            print( "  ", self.get_video_details(vid) )

    def play_video(self, video_id):
        """Plays the respective video.
        Args:
            video_id: The video_id to be played.
        """
        # print("play_video needs implementation")

        video = self._video_library.get_video(video_id)
        if video != None:

            if(video.flagged == None):
                if self.vid_stages.status != video_state.Stop: 
                    self.stop_video() 

                self.vid_stages.set_video(video, video_state.Playing)
            else:
                print("Cannot play video: Video is currently flagged (reason: "+ video.flagged +")")

        else:
            print("Cannot play video: Video does not exist")

    def stop_video(self):
        """Stops the current video."""
        # print("stop_video needs implementation")

        if self.vid_stages.status != video_state.Stop:
            self.vid_stages.set_status(video_state.Stop)

        else:
            print("Cannot stop video: No video is currently playing")

    def play_random_video(self):
        """Plays a random video from the video library."""
        # print("play_random_video needs implementation")
        videos = self._video_library.get_all_videos()

        if len([x for x in videos if x.flagged == None]) == 0:
            print("No videos available")
            return

        vid = videos[ random.randint(0, len(videos)-1) ]
        self.play_video(vid._video_id)

    def pause_video(self):
        """Pauses the current video."""
        # print("pause_video needs implementation")
        
        if self.vid_stages.video != None:
            if( self.vid_stages.status != video_state.Pause ):
                self.vid_stages.set_status(video_state.Pause)
            else:
                print("Video already paused:", self.vid_stages.video._title)
        
        else:
            print("Cannot pause video: No video is currently playing")

    def continue_video(self):
        """Resumes playing the current video."""
        # print("continue_video needs implementation")

        if self.vid_stages.video != None:
            if self.vid_stages.status == video_state.Pause:
                self.vid_stages.set_status(video_state.Continue)
            else: 
                 print("Cannot continue video: Video is not paused")
        else:
            print("Cannot continue video: No video is currently playing")

    def show_playing(self):
        """Displays video currently playing."""
        # print("show_playing needs implementation")
        if self.vid_stages.video != None:
            if self.vid_stages.status != video_state.Pause:
                print("Currently playing:", self.get_video_details(self.vid_stages.video))
            else:
                print("Currently playing:", self.get_video_details(self.vid_stages.video), "- PAUSED")

        else:
            print("No video is currently playing")
    #Part2

    def playlist_avail(self, name):
        return name in self.playlists.keys()

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.
        Args:
            playlist_name: The playlist name.
        """
        # print("create_playlist needs implementation")

        pl_name = playlist_name.lower()
        if pl_name in self.playlists.keys():
            print("Cannot create playlist: A playlist with the same name already exists")
        else:
            self.playlists[ pl_name ] = []
            self.userWrittenStylePlaylists[pl_name] = playlist_name # for later user to display the playlist
            print("Successfully created new playlist:", self.userWrittenStylePlaylists[pl_name])

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.
        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        # print("add_to_playlist needs implementation")

        pl_name = playlist_name.lower()
        video = self._video_library.get_video(video_id)

        if self.playlist_avail(pl_name):

            if video != None:
                if(video.flagged == None):
                    if video in self.playlists[ pl_name ]:
                        print("Cannot add video to " + playlist_name + ": Video already added")
                    else:
                        self.playlists[ pl_name ].append( video )
                        print("Added video to " + playlist_name + ":", video._title)
                else:
                    print("Cannot add video to " + playlist_name + ": Video is currently flagged (reason: " + \
                        video.flagged + ")")
            else:
                print("Cannot add video to " + playlist_name + ": Video does not exist")
    
        else:
            print("Cannot add video to " + playlist_name + ": Playlist does not exist")

    def show_all_playlists(self):
        """Display all playlists."""
        # print("show_all_playlists needs implementation")
        if(len(self.playlists.keys()) == 0): #means no playlist added
            print("No playlists exist yet")

        else:
            print("Showing all playlists: ")
            for playlist in sorted(self.playlists.keys()):
                print( "   " + self.userWrittenStylePlaylists[playlist.lower()])
    
    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.
        Args:
            playlist_name: The playlist name.
        """
        # print("show_playlist needs implementation")
        pl_name = playlist_name.lower()

        if self.playlist_avail(pl_name):
            videos = self.playlists[pl_name]
            print("Showing playlist:", playlist_name)

            if len(videos) != 0 :
                for vid in videos:
                    print( "  ", self.get_video_details(vid))

            else:
                print( "  ", "No videos here yet")
        else:
            print( "Cannot show playlist " + playlist_name + ": Playlist does not exist")

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.
        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        # print("remove_from_playlist needs implementation")
        
        pl_name = playlist_name.lower()
        video = self._video_library.get_video(video_id)

        if self.playlist_avail(pl_name):

            if video != None:
                if video in self.playlists[ pl_name ]:
                    print("Removed video from " + playlist_name + ":", video._title)
                    self.playlists[ pl_name ].remove( video )
                else:
                    print("Cannot remove video from " + playlist_name + ": Video is not in playlist")
            else:
                print("Cannot remove video from " + playlist_name + ": Video does not exist")
        else:
            print("Cannot remove video from " + playlist_name + ": Playlist does not exist")

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.
        Args:
            playlist_name: The playlist name.
        """
        # print("clears_playlist needs implementation")
        
        pl_name = playlist_name.lower()
        if self.playlist_avail(pl_name):
            self.playlists[ pl_name ] = []
            print("Successfully removed all videos from " + playlist_name )
        else:
            print("Cannot clear playlist " + playlist_name + ": Playlist does not exist")

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.
        Args:
            playlist_name: The playlist name.
        """
        # print("deletes_playlist needs implementation")
        
        pl_name = playlist_name.lower()
        if self.playlist_avail(pl_name):
            self.playlists.pop( pl_name )
            print("Deleted playlist: " + pl_name )
        else:
            print("Cannot delete playlist " + pl_name + ": Playlist does not exist")

    
    # PART 3
    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.
        Args:
            search_term: The query to be used in search.
        """
        # print("search_videos needs implementation")
        all_videos = self._video_library.get_all_videos()

        search_vid = []
        for video in all_videos:
            if(video.flagged == None):
                if search_term.lower() in video._title.lower():
                    search_vid.append(video)

        if(len(search_vid) != 0):
            i = 1
            print("Here are the results for "+  search_term + ":")
            for svid in search_vid:
                print("  ", str(i) + ")", self.get_video_details(svid))
                i+=1

            print( "Would you like to play any of the above? If yes, specify the number of the video.")
            print( "If your answer is not a valid number, we will assume it's a no.")   

            val = input()
            if(val.isnumeric()):
                _index = int(val)
                if _index > 0 and _index <= len(search_vid):
                    self.play_video(search_vid[_index-1]._video_id)
        else:
            print("No search results for", search_term)

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.
        Args:
            video_tag: The video tag to be used in search.
        """
        # print("search_videos_tag needs implementation")
        all_videos = self._video_library.get_all_videos()

        search_vid = []
        for video in all_videos:
            if(video.flagged == None):
                if video_tag in video._tags:
                    search_vid.append(video)

        if(len(search_vid) != 0):
            i = 1
            print("Here are the results for "+  video_tag + ":")
            for svid in search_vid:
                print("  ", str(i) + ")", self.get_video_details(svid))
                i+=1

            print( "Would you like to play any of the above? If yes, specify the number of the video.")
            print( "If your answer is not a valid number, we will assume it's a no.")   

            val = input()
            if(val.isnumeric()):
                _index = int(val)
                if _index > 0 and _index <= len(search_vid):
                    self.play_video(search_vid[_index-1]._video_id)
        else:
            print("No search results for", video_tag)

    #PART 4
    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.
        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        # print("flag_video needs implementation")
        video = self._video_library.get_video(video_id)

        if(flag_reason == ""):
            flag_reason = "Not supplied"

        if video != None:
            if(video.flagged == None):
                if(self.vid_stages.video != None):
                    if(video_id == self.vid_stages.video._video_id):
                        if(self.vid_stages.status == video_state.Playing or self.vid_stages.status == video_state.Pause):
                            self.vid_stages.set_status(video_state.Stop)
                
                video.flagged = flag_reason
                print("Successfully flagged video:", video._title + " (reason: "+ video.flagged + ")")

            else:
                print("Cannot flag video: Video is already flagged")
        
        else:
            print("Cannot flag video: Video does not exist")

    def allow_video(self, video_id):
        """Removes a flag from a video.
        Args:
            video_id: The video_id to be allowed again.
        """
        # print("allow_video needs implementation")

        video = self._video_library.get_video(video_id)
        
        if video != None:
            if(video.flagged != None):
                video.flagged = None
                print("Successfully removed flag from video:", video._title)

            else:
                print("Cannot remove flag from video: Video is not flagged")
        
        else:
            print("Cannot remove flag from video: Video does not exist")
