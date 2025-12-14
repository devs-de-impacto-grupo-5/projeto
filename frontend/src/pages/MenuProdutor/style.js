import styled from 'styled-components';
import { neutral, darkPurple, lightYellow, darkYellow, lightGreen } from '../../constants/colors';

export const Container = styled.div`
  padding: 20px;
  background-color: ${neutral};
  min-height: 100vh;
  position: relative;
`;

export const Header = styled.div`
  display: flex;
  justify-content: flex-end;
  margin-bottom: 20px;
`;

export const HelpButton = styled.button`
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: ${lightYellow};
  border: none;
  color: ${darkYellow};
  cursor: pointer;

  &:hover {
    opacity: 0.9;
  }
`;

export const UserSection = styled.div`
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 32px;
`;

export const Avatar = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background-color: ${lightGreen};
  flex-shrink: 0;
`;

export const UserInfo = styled.div`
  display: flex;
  flex-direction: column;
  gap: 2px;
`;

export const Greeting = styled.p`
  font-size: 14px;
  font-weight: 400;
  color: ${darkPurple};
  margin: 0;
`;

export const UserName = styled.h2`
  font-size: 18px;
  font-weight: 700;
  color: ${darkPurple};
  margin: 0;
`;

export const MenuTitle = styled.h1`
  font-size: 20px;
  font-weight: 700;
  color: ${darkPurple};
  margin: 0 0 4px 0;
`;

export const MenuSubtitle = styled.p`
  font-size: 14px;
  font-weight: 400;
  color: ${darkPurple};
  margin: 0 0 24px 0;
`;

export const CardsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
`;
