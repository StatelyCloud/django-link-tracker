import os
import asyncio
import logging
from typing import Optional, List
from uuid import UUID
from generated.stately_item_types import Client, Link, Profile, key_path
from statelydb.src.errors import StatelyError

logger = logging.getLogger(__name__)


class StatelyClient:
    def __init__(self):
        self.store_id = os.environ.get('STATELY_STORE_ID')
        
        if not self.store_id:
            raise ValueError("STATELY_STORE_ID environment variable is required")
        
        # Configure client with AWS US East 1 region
        self.client = Client(
            store_id=self.store_id,
            region="us-east-1",
        )



stately_client = StatelyClient()


async def get_profile_and_links(slug: str) -> tuple[Optional[Profile], List[Link]]:
    """Get a profile and all its links with a single list call."""
    try:
        prefix = key_path("/p-{slug}", slug=slug)
        list_resp = await stately_client.client.begin_list(prefix, limit=100)
        
        profile = None
        links = []

        async for item in list_resp:
            if isinstance(item, Profile):
                profile = item
            elif isinstance(item, Link):
                links.append(item)
        
        return profile, links
    except StatelyError as e:
        logger.error(f"Error getting profile and links for '{slug}': {e}")
        return None, []



async def get_link_by_id(link_id: int, profile_slug: str) -> Optional[Link]:
    """Get a specific link by ID within a profile."""
    try:
        kp = key_path("/p-{slug}/l-{id}", slug=profile_slug, id=link_id)
        link = await stately_client.client.get(Link, kp)
        return link if isinstance(link, Link) else None
    except StatelyError as e:
        logger.error(f"Error getting link by id '{link_id}' for profile '{profile_slug}': {e}")
        return None


async def create_link(profile_slug: str, title: str, url: str, emoji: str = "🔗", link_type: str = "other", description: str = "") -> Link:
    """Create a new link for a profile."""
    _, existing_links = await get_profile_and_links(profile_slug)
    
    max_order = max([link.order for link in existing_links], default=0)
    
    link = Link(
        profile_id=profile_slug,
        title=title,
        url=url,
        emoji=emoji,
        link_type=link_type,
        description=description,
        is_active=True,
        order=max_order + 1,
        click_count=1
    )
    
    return await stately_client.client.put(link)




async def delete_link(link_id: int, profile_slug: str) -> None:
    """Delete a link by ID."""
    key_path_str = f"/p-{profile_slug}/l-{link_id}"
    kp = key_path(key_path_str)
    await stately_client.client.delete(kp)


async def create_profile(name: str, slug: str, profile_image: str = "🌟") -> Profile:
    """Create a new profile."""
    profile = Profile(
        id=slug,
        full_name=name,
        slug=slug,
        profile_image=profile_image,
        bio="Welcome to my profile!",
        is_active=True,
        view_count=1
    )
    
    return await stately_client.client.put(profile)


async def increment_link_clicks(link_id: int, profile_slug: str) -> Optional[Link]:
    """Increment click count for a link using transaction."""
    try:
        txn = await stately_client.client.transaction()
        async with txn:
            # Get the link item
            kp = key_path("/p-{slug}/l-{id}", slug=profile_slug, id=link_id)
            link = await txn.get(Link, kp)
            
            if not link:
                logger.warning(f"Link '{link_id}' not found in profile '{profile_slug}' for incrementing clicks")
                return None
            
            # Update the click count
            link.click_count += 1
            await txn.put(link)
        
        # Return the updated link from transaction result
        return txn.result.puts[0]
    except StatelyError as e:
        logger.error(f"Error incrementing clicks for link '{link_id}' in profile '{profile_slug}': {e}")
        return None


async def increment_profile_views(profile_slug: str) -> Optional[Profile]:
    """Increment view count for a profile using transaction."""
    try:
        txn = await stately_client.client.transaction()
        async with txn:
            # Get the profile item
            kp = key_path("/p-{slug}", slug=profile_slug)
            profile = await txn.get(Profile, kp)
            
            if not profile:
                logger.warning(f"Profile '{profile_slug}' not found for incrementing views")
                return None
            
            # Update the view count
            profile.view_count += 1
            await txn.put(profile)
        
        # Return the updated profile from transaction result
        return txn.result.puts[0]
    except StatelyError as e:
        logger.error(f"Error incrementing views for profile '{profile_slug}': {e}")
        return None


async def rename_profile(profile_slug: str, new_name: str) -> Optional[Profile]:
    """Rename a profile using transaction."""
    try:
        txn = await stately_client.client.transaction()
        async with txn:
            # Get the profile item
            kp = key_path("/p-{slug}", slug=profile_slug)
            profile = await txn.get(Profile, kp)
            
            if not profile:
                logger.warning(f"Profile '{profile_slug}' not found for renaming")
                return None
            
            # Update the name
            profile.full_name = new_name
            await txn.put(profile)
        
        # Return the updated profile from transaction result
        return txn.result.puts[0]
    except StatelyError as e:
        logger.error(f"Error renaming profile '{profile_slug}' to '{new_name}': {e}")
        return None


async def update_profile_bio(profile_slug: str, new_bio: str) -> Optional[Profile]:
    """Update a profile's bio using transaction."""
    try:
        txn = await stately_client.client.transaction()
        async with txn:
            # Get the profile item
            kp = key_path("/p-{slug}", slug=profile_slug)
            profile = await txn.get(Profile, kp)
            
            if not profile:
                logger.warning(f"Profile '{profile_slug}' not found for bio update")
                return None
            
            # Update the bio
            profile.bio = new_bio
            await txn.put(profile)
        
        # Return the updated profile from transaction result
        return txn.result.puts[0]
    except StatelyError as e:
        logger.error(f"Error updating bio for profile '{profile_slug}': {e}")
        return None


async def update_link_order(link_id: int, order: int, profile_slug: str) -> Optional[Link]:
    """Update the order of a link using transaction."""
    try:
        txn = await stately_client.client.transaction()
        async with txn:
            # Get the link item
            kp = key_path("/p-{slug}/l-{id}", slug=profile_slug, id=link_id)
            link = await txn.get(Link, kp)
            
            if not link:
                logger.warning(f"Link '{link_id}' not found in profile '{profile_slug}' for updating order")
                return None
            
            # Update the order
            link.order = order
            await txn.put(link)
        
        # Return the updated link from transaction result
        return txn.result.puts[0]
    except StatelyError as e:
        logger.error(f"Error updating order for link '{link_id}' in profile '{profile_slug}': {e}")
        return None


