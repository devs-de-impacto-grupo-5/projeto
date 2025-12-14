import styled from 'styled-components';
import { neutral, darkPurple, lightGreen, lightPurple } from '../../constants/colors';

export const Container = styled.div`
  background-color: ${neutral}; // Using the neutral color from constants
  min-height: 100vh;
  width: 100vw;
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  font-family: 'Outfit', sans-serif; // Assuming fonts are set globally or imported
`;

export const Navbar = styled.nav`
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 60px;
  width: 100%;
  box-sizing: border-box;
  z-index: 20;
`;

export const LogoContainer = styled.div`
  img {
    height: 40px; 
  }
`;

export const NavLinks = styled.div`
  display: flex;
  gap: 40px;

  a {
    text-decoration: none;
    color: #333; // Default dark text
    font-weight: 600;
    font-size: 1rem;
    transition: color 0.2s;
    cursor: pointer;
    
    &:hover {
        color: ${darkPurple};
    }
  }
`;

export const MainContent = styled.main`
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 100px;
  z-index: 10;
  width: 100%;
  box-sizing: border-box;

  @media (max-width: 1024px) {
    flex-direction: column;
    padding: 40px 20px;
    text-align: center;
    justify-content: center;
    gap: 40px;
  }
`;

export const TextSection = styled.div`
  max-width: 50%;
  
  @media (max-width: 1024px) {
    max-width: 100%;
  }
`;

export const Headline = styled.h1`
  font-size: 3.5rem;
  color: ${darkPurple}; // Based on image
  font-weight: 800;
  line-height: 1.2;
  margin-bottom: 40px;
  
  // Customizing highlights based on image
  // "Vital para quem produz" -> "produz" is highlight? 
  // Actually text "Vital para quem" is dark purple. "produz" has a Comma after it.
  
  strong {
     color: inherit;
  }
`;

export const HighlightLighter = styled.span`
  color: #CDB9E7; // Lighter purple for "aprende" maybe? Or lightPurple from constants
  // referencing the image, "aprende" is lighter purple.
  color: ${lightPurple}; // Let's try constant first
`;

export const HighlightDarker = styled.span`
  color: ${lightPurple}; // "produz" also looks colored?
  // In the image: "Vital para quem" (Dark), "produz" (Lighter?), "essencial para quem" (Dark), "aprende" (Lighter)
  // Actually "produz" looks like a medium purple, "aprende" looks lighter.
  // I will use lightPurple for both initially or tweak.
`;


export const CallActionButton = styled.button`
  background-color: white;
  color: #333;
  border: none;
  padding: 18px 40px;
  border-radius: 50px;
  font-size: 1.2rem;
  font-weight: 500;
  box-shadow: 0 5px 20px rgba(0,0,0,0.05); // Soft shadow
  cursor: pointer;
  transition: all 0.2s ease;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0,0,0,0.1);
  }
`;

export const ImageSection = styled.div`
  position: relative;
  width: 45%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;

  @media (max-width: 1024px) {
    width: 80%;
  }
`;

export const CircleWrapper = styled.div`
  width: 500px;
  height: 500px;
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;

  @media (max-width: 768px) {
    width: 350px;
    height: 350px;
  }
`;

export const PersonImg = styled.img`
  width: 100%;
  height: auto;
  object-fit: contain;
`;

// Background Blob Top Right
export const TopRightBlob = styled.img`
  position: absolute;
  top: -18px;
  right: -32px;
  width: clamp(170px, 10vw, 220px);
  height: auto;
  z-index: 0;
  pointer-events: none;
  user-select: none;
`;

// Background Blob Bottom Left
export const BottomLeftBlob = styled.img`
  position: absolute;
  bottom: -18px;
  left: -32px;
  width: clamp(170px, 10vw, 220px);
  height: auto;
  z-index: 0;
  pointer-events: none;
  user-select: none;
`;
